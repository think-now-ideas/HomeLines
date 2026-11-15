"""Geplante PPPoE-Neueinwahl per SSH."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import logging
import re
import shlex

import asyncssh

from .const import (
    METHOD_IP_LINK,
    METHOD_PPPD_HUP,
    RECONNECT_POLL,
    RECONNECT_WAIT,
    RESULT_ERROR,
    RESULT_NEW_IP,
    RESULT_NO_EFFECT,
    RESULT_SAME_IP,
)

_LOGGER = logging.getLogger(__name__)

_IFACE_RE = re.compile(r"^[A-Za-z0-9._-]{1,15}$")
_INET_RE = re.compile(r"\binet (\d{1,3}(?:\.\d{1,3}){3})")
_LINK_RE = re.compile(r"^\d+:\s+([A-Za-z0-9._-]+)[:@]", re.MULTILINE)


class SSHError(Exception):
    """SSH fehlgeschlagen."""


class SSHAuthError(SSHError):
    """Anmeldung abgelehnt."""


class SSHHostKeyError(SSHError):
    """Der Router meldet sich mit einem anderen Fingerabdruck als gespeichert.

    Das Passwort wurde in diesem Fall NICHT gesendet. ``new_key`` ist der Schlüssel, den das Gerät
    jetzt zeigt (oder None, falls er nicht gelesen werden konnte)."""

    def __init__(self, new_key: str | None) -> None:
        self.new_key = new_key
        self.fingerprint = fingerprint(new_key) if new_key else None
        super().__init__("Der Router meldet sich mit einem anderen Fingerabdruck als gespeichert – "
                         "Passwort nicht gesendet, Neueinwahl gesperrt. Unter Einstellungen → Reparaturen bestätigen.")


def fingerprint(key: str | None) -> str | None:
    """SHA256-Fingerabdruck eines öffentlichen Schlüssels im OpenSSH-Format (wie ``ssh-keygen -l``)."""
    if not key:
        return None
    try:
        return asyncssh.import_public_key(key).get_fingerprint("sha256")
    except (asyncssh.KeyImportError, ValueError):
        return None


def validate_interface(name: str) -> str:
    if not _IFACE_RE.match(name or ""):
        raise ValueError(f"Ungültiger Schnittstellenname: {name!r}")
    return name


def build_command(method: str, iface: str) -> str:
    iface = shlex.quote(validate_interface(iface))
    if method == METHOD_PPPD_HUP:
        # killall fehlt auf neueren UniFi-OS-Versionen – deshalb pkill bzw. kill über pidof
        return ("P=$(pidof pppd); [ -n \"$P\" ] || { echo 'pppd läuft nicht'; exit 3; }; "
                "kill -HUP $P")
    if method == METHOD_IP_LINK:
        return f"ip link set dev {iface} down && sleep 2 && ip link set dev {iface} up"
    raise ValueError(method)


def parse_ipv4(text: str) -> str | None:
    m = _INET_RE.search(text)
    return m.group(1) if m else None


def parse_ppp(text: str) -> list[str]:
    return [n for n in _LINK_RE.findall(text) if n.startswith("ppp")]


@dataclass
class LinkState:
    ip: str | None
    ifindex: str | None


class SSHClient:
    """Kurze SSH-Verbindung je Vorgang – nur zu einem Router mit bekanntem Fingerabdruck.

    ``host_key`` ist der gespeicherte öffentliche Schlüssel des Routers (OpenSSH-Zeile). Fehlt er,
    liest der Client ihn beim ersten Verbinden OHNE Anmeldung aus und merkt ihn sich in ``learned``
    (der Aufrufer speichert ihn dauerhaft). Das Passwort geht nur an ein Gerät, das genau diesen
    Schlüssel beweist; ein anderer Schlüssel führt zu ``SSHHostKeyError``."""

    def __init__(self, host: str, port: int, user: str, password: str, host_key: str | None = None) -> None:
        self.host, self.port, self.user, self.password = host, port, user, password
        self.host_key = host_key
        self.learned: str | None = None   # beim ersten Verbinden gelernter Schlüssel
        self.connected = False            # mindestens eine Anmeldung hat geklappt

    async def fetch_host_key(self) -> str:
        """Öffentlichen Schlüssel des Geräts lesen, ohne sich anzumelden (kein Passwort)."""
        try:
            async with asyncio.timeout(15):
                key = await asyncssh.get_server_host_key(self.host, self.port)
        except (OSError, asyncssh.Error, TimeoutError) as err:
            raise SSHError(str(err)) from err
        if key is None:
            raise SSHError("Router hat keinen Schlüssel gemeldet")
        return key.export_public_key("openssh").decode().strip()

    async def run(self, command: str, timeout: int = 30) -> tuple[int, str]:
        key = self.host_key or self.learned
        if key is None:
            key = self.learned = await self.fetch_host_key()
        try:
            trusted = asyncssh.import_public_key(key)
        except (asyncssh.KeyImportError, ValueError) as err:
            raise SSHError(f"Gespeicherter Router-Fingerabdruck ist ungültig: {err}") from err
        try:
            async with asyncio.timeout(timeout + 15):
                async with asyncssh.connect(
                    self.host, port=self.port, username=self.user, password=self.password,
                    known_hosts=([trusted], [], []), connect_timeout=15) as conn:
                    self.connected = True
                    res = await conn.run(command, check=False, timeout=timeout)
                    return res.exit_status or 0, str(res.stdout or "") + str(res.stderr or "")
        except (asyncssh.HostKeyNotVerifiable, asyncssh.KeyExchangeFailed) as err:
            # Anderer Schlüssel – oder ein ganz anderer Schlüsseltyp, dann scheitert schon der
            # Schlüsselaustausch. In beiden Fällen wurde KEIN Passwort gesendet.
            try:
                new = await self.fetch_host_key()
            except SSHError:
                new = None
            if isinstance(err, asyncssh.KeyExchangeFailed) and new is not None and fingerprint(new) == trusted.get_fingerprint("sha256"):
                raise SSHError(str(err)) from err   # gleicher Schlüssel, anderes Problem
            raise SSHHostKeyError(new) from err
        except asyncssh.PermissionDenied as err:
            raise SSHAuthError(str(err)) from err
        except (OSError, asyncssh.Error, TimeoutError) as err:
            raise SSHError(str(err)) from err

    async def interfaces(self) -> list[str]:
        _, out = await self.run("ip -o link show")
        return parse_ppp(out)

    async def link_state(self, iface: str) -> LinkState:
        i = shlex.quote(validate_interface(iface))
        _, out = await self.run(f"ip -4 addr show dev {i} 2>/dev/null; echo IDX=$(cat /sys/class/net/{i}/ifindex 2>/dev/null)")
        idx = re.search(r"IDX=(\d*)", out)
        return LinkState(parse_ipv4(out), idx.group(1) if idx and idx.group(1) else None)

    async def reconnect(self, method: str, iface: str) -> tuple[str, str | None, str | None]:
        """Neueinwahl auslösen und Ergebnis bestimmen: (Ergebnis, alte IP, neue IP)."""
        before = await self.link_state(iface)
        if before.ifindex is None:
            raise SSHError(f"Schnittstelle {iface} gibt es auf dem Router nicht – unter Neueinwahl die richtige wählen")
        code, out = await self.run(build_command(method, iface))
        if code != 0:
            raise SSHError(f"Befehl fehlgeschlagen ({code}): {out.strip()[:200] or 'keine Ausgabe'}")
        seen_down = False
        loop = asyncio.get_running_loop()
        deadline = loop.time() + RECONNECT_WAIT
        while loop.time() < deadline:
            await asyncio.sleep(RECONNECT_POLL)
            try:
                now = await self.link_state(iface)
            except SSHError:
                continue
            if now.ip is None or now.ifindex is None:
                seen_down = True
                continue
            if now.ifindex != before.ifindex or seen_down:
                return (RESULT_NEW_IP if now.ip != before.ip else RESULT_SAME_IP), before.ip, now.ip
            if now.ip != before.ip:
                return RESULT_NEW_IP, before.ip, now.ip
        return (RESULT_ERROR if seen_down else RESULT_NO_EFFECT), before.ip, None
