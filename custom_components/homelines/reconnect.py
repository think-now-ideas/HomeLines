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
    """Kurze SSH-Verbindung je Vorgang."""

    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self.host, self.port, self.user, self.password = host, port, user, password

    async def run(self, command: str, timeout: int = 30) -> tuple[int, str]:
        try:
            async with asyncio.timeout(timeout + 15):
                async with asyncssh.connect(
                    self.host, port=self.port, username=self.user, password=self.password,
                    known_hosts=None, connect_timeout=15) as conn:
                    res = await conn.run(command, check=False, timeout=timeout)
                    return res.exit_status or 0, str(res.stdout or "") + str(res.stderr or "")
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
