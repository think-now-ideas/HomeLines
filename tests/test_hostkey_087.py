"""0.8.7: SSH nur noch zum Router mit bekanntem Fingerabdruck.

Getestet gegen echte SSH-Server (asyncssh) auf 127.0.0.1 – die Server zählen mit, ob ein
Passwort bei ihnen ankommt.
"""

from __future__ import annotations

from unittest.mock import patch

import asyncssh
import pytest
from homeassistant.helpers import issue_registry as ir
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.homelines import repairs
from custom_components.homelines.config_flow import validate_ssh
from custom_components.homelines.const import DOMAIN
from custom_components.homelines.reconnect import SSHAuthError, SSHClient, SSHHostKeyError, fingerprint

from test_homelines import BASE, OPTIONS

PW = "geheim"


class _Server:
    """SSH-Server, der jedes angekommene Passwort mitschreibt."""

    def __init__(self):
        self.passwords: list[str] = []
        self.acceptor = None

    async def start(self, keys, port=0):
        srv = self

        class Srv(asyncssh.SSHServer):
            def begin_auth(self, username):
                return True

            def password_auth_supported(self):
                return True

            def validate_password(self, username, password):
                srv.passwords.append(password)
                return password == PW

        async def handle(proc):
            proc.stdout.write("inet 203.0.113.7/32 scope global ppp1\nIDX=7\n")
            proc.exit(0)

        self.acceptor = await asyncssh.listen("127.0.0.1", port, server_host_keys=keys, server_factory=Srv,
                                              process_factory=handle)
        return self.acceptor.sockets[0].getsockname()[1]

    def stop(self):
        self.acceptor.close()


@pytest.fixture
def keys(socket_enabled):
    """Schlüssel für die Test-Server; ``socket_enabled`` erlaubt echte Verbindungen auf 127.0.0.1."""
    return {"ed": asyncssh.generate_private_key("ssh-ed25519"), "rsa": asyncssh.generate_private_key("ssh-rsa"),
            "fremd": asyncssh.generate_private_key("ssh-ed25519"),
            "fremd_rsa": asyncssh.generate_private_key("ssh-rsa")}


async def test_client_learns_and_enforces(keys):
    real = _Server()
    port = await real.start([keys["ed"], keys["rsa"]])
    c = SSHClient("127.0.0.1", port, "root", PW)
    assert (await c.run("x"))[0] == 0
    assert c.connected and c.learned
    pinned = c.learned
    assert fingerprint(pinned) in (keys["ed"].get_fingerprint(), keys["rsa"].get_fingerprint())
    assert (await SSHClient("127.0.0.1", port, "root", PW, host_key=pinned).run("x"))[0] == 0
    with pytest.raises(SSHAuthError):
        await SSHClient("127.0.0.1", port, "root", "falsch", host_key=pinned).run("x")
    real.stop()

    # Fremdes Gerät auf derselben Adresse: gleicher und anderer Schlüsseltyp – nie ein Passwort
    for k in ("fremd", "fremd_rsa"):
        fake = _Server()
        await fake.start([keys[k]], port)
        with pytest.raises(SSHHostKeyError) as err:
            await SSHClient("127.0.0.1", port, "root", PW, host_key=pinned).run("x")
        assert err.value.fingerprint == keys[k].get_fingerprint()
        assert fake.passwords == []
        fake.stop()


async def test_hub_pins_blocks_and_repair(hass, unifi, ping, keys):
    real = _Server()
    port = await real.start([keys["ed"]])
    data = {**BASE, "reconnect_enabled": True, "ssh_host": "127.0.0.1", "ssh_port": port, "ssh_user": "root",
            "ssh_password": PW, "ppp_interface": "ppp1", "reconnect_method": "pppd_hup", "reconnect_time": "04:00:00"}
    entry = MockConfigEntry(domain=DOMAIN, title="HomeLines", data=data, options=OPTIONS)
    entry.add_to_hass(hass)
    hass.states.async_set("sensor.unifi_active_wan_id", "WAN2")

    async def fake_reconnect(self, method, iface):
        await self.run("ip -4 addr show dev ppp1")   # echte Anmeldung am Test-Server
        return "ok_same_ip", "203.0.113.7", "203.0.113.7"

    issue_id = f"ssh_host_key_changed_{entry.entry_id}"
    with patch("custom_components.homelines.reconnect.SSHClient.reconnect", fake_reconnect):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        hub = hass.data[DOMAIN][entry.entry_id]

        # 1) Erste Neueinwahl: Fingerabdruck wird gelernt und gespeichert
        assert await hub.async_reconnect() == "ok_same_ip"
        assert hub.data["ssh"]["fingerprint"] == keys["ed"].get_fingerprint()
        assert hub.ssh_pin() is not None
        assert real.passwords == [PW]
        real.stop()

        # 2) Anderes Gerät antwortet: gesperrt, Passwort nicht gesendet, Reparatur-Hinweis
        fake = _Server()
        await fake.start([keys["fremd"]], port)
        assert await hub.async_reconnect() == "error"
        assert fake.passwords == []
        assert "Fingerabdruck" in hub.data["reconnect"]["error"]
        issue = ir.async_get(hass).async_get_issue(DOMAIN, issue_id)
        assert issue is not None and issue.is_fixable
        assert issue.translation_placeholders["new"] == keys["fremd"].get_fingerprint()
        assert hub.data["ssh"]["fingerprint"] == keys["ed"].get_fingerprint()   # alter bleibt bis zur Bestätigung

        # 3) Nutzer bestätigt im Reparatur-Dialog
        flow = await repairs.async_create_fix_flow(hass, issue_id, issue.data)
        flow.hass, flow.handler, flow.flow_id, flow.issue_id = hass, DOMAIN, "t1", issue_id
        form = await flow.async_step_init()
        assert form["type"] == "form" and form["description_placeholders"]["new"] == keys["fremd"].get_fingerprint()
        done = await flow.async_step_confirm({})
        assert done["type"] == "create_entry"
        assert ir.async_get(hass).async_get_issue(DOMAIN, issue_id) is None
        assert hub.data["ssh"]["fingerprint"] == keys["fremd"].get_fingerprint()

        # 4) Danach klappt die Neueinwahl mit dem neuen Fingerabdruck
        assert await hub.async_reconnect() == "ok_same_ip"
        assert fake.passwords == [PW]
        fake.stop()

        # 5) Neue Adresse in den Optionen → alter Fingerabdruck gilt dort nicht
        assert hub.ssh_pin("192.168.1.99", port) is None


async def test_options_validation_uses_pin(keys):
    real = _Server()
    port = await real.start([keys["ed"]])
    data = {"reconnect_enabled": True, "reconnect_method": "pppd_hup", "ssh_host": "127.0.0.1", "ssh_port": port,
            "ssh_user": "root", "ssh_password": PW, "ppp_interface": "ppp1"}
    good = keys["ed"].export_public_key("openssh").decode()
    bad = keys["fremd"].export_public_key("openssh").decode()
    assert await validate_ssh(data, good) in ({}, {"ppp_interface": "interface_not_found"})
    assert await validate_ssh(data, bad) == {"base": "ssh_hostkey"}
    assert real.passwords == [PW]   # nur die Prüfung mit dem richtigen Fingerabdruck hat ein Passwort gesendet
    real.stop()
