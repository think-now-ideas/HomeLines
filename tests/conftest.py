"""Test-Fixtures: simulierter UniFi-Controller und Ping."""

from __future__ import annotations

import copy
from unittest.mock import patch

import pytest

from custom_components.homelines import router as router_mod
from custom_components.homelines.monitor import PingResult

pytest_plugins = ["pytest_homeassistant_custom_component"]


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


class FakeUnifi:
    def __init__(self):
        self.key = "secret"
        self.networks = [
            {"_id": "wan1", "purpose": "wan", "name": "Internet 1", "wan_networkgroup": "WAN"},
            {"_id": "wan2", "purpose": "wan", "name": "DSL", "wan_networkgroup": "WAN2"},
            {"_id": "wan3", "purpose": "wan", "name": "5G Backup", "wan_networkgroup": "WAN3"},
            {"_id": "lan", "purpose": "corporate", "name": "Default"},
            {"_id": "iot", "purpose": "corporate", "name": "IoT"},
            {"_id": "guest", "purpose": "guest", "name": "Gäste"},
        ]
        self.online = [
            {"mac": "AA:00:00:00:00:01", "name": "Home Assistant", "network_id": "lan", "ip": "192.168.1.10"},
            {"mac": "aa:00:00:00:00:02", "hostname": "handy", "network_id": "lan"},
            {"mac": "aa:00:00:00:00:03", "name": "Shelly", "network_id": "iot"},
            {"mac": "aa:00:00:00:00:04", "name": "Gast-Handy", "network": "Gäste"},
        ]
        self.known = [{"mac": "aa:00:00:00:00:05", "name": "NAS", "last_seen": 9999999999},
                      {"mac": "aa:00:00:00:00:06", "name": "Alt", "last_seen": 1}]
        self.routes: list[dict] = []
        self.calls: list[tuple] = []

    async def request(self, adapter, method, path, json=None):
        self.calls.append((method, path))
        if adapter.config["api_key"] != self.key:
            raise router_mod.RouterAuthError("401")
        if path.endswith("rest/networkconf"):
            return copy.deepcopy(self.networks)
        if path.endswith("stat/sta"):
            return copy.deepcopy(self.online)
        if path.endswith("rest/user"):
            return copy.deepcopy(self.known)
        if path.endswith("/trafficroutes") and method == "GET":
            return copy.deepcopy(self.routes)
        if path.endswith("/trafficroutes") or "/trafficroutes/" in path:
            if method in ("POST", "PUT"):
                self._check_ids(json)
        if path.endswith("/trafficroutes") and method == "POST":
            r = {**json, "_id": f"r{len(self.routes) + 1}"}
            self.routes.append(r)
            return r
        if "/trafficroutes/" in path and method == "PUT":
            rid = path.rsplit("/", 1)[1]
            for i, r in enumerate(self.routes):
                if r["_id"] == rid:
                    self.routes[i] = {**json, "_id": rid}
            return self.routes[0]
        if "/trafficroutes/" in path and method == "DELETE":
            rid = path.rsplit("/", 1)[1]
            self.routes = [r for r in self.routes if r["_id"] != rid]
            return None
        raise router_mod.RouterError(f"unknown {method} {path}")

    def _check_ids(self, body):
        """Wie UniFi: unbekannte Netz-IDs lehnt der Controller mit HTTP 400 ab."""
        known = {n["_id"] for n in self.networks}
        ids = [body.get("network_id")] + [t["network_id"] for t in body.get("target_devices", []) if "network_id" in t]
        if any(i and i not in known for i in ids):
            raise router_mod.RouterError(
                'HTTP 400: {"meta":{"rc":"error","msg":"api.err.InvalidNetworkConfId"},"data":[]}')

    def recreate(self, old_id, new_id):
        """UniFi legt eine Konfiguration neu an: gleicher Name, neue ID."""
        for n in self.networks:
            if n["_id"] == old_id:
                n["_id"] = new_id
        for c in self.online:
            if c.get("network_id") == old_id:
                c["network_id"] = new_id

    def route_targets(self):
        r = self.routes[0]
        return r["enabled"], sorted(
            t.get("client_mac") or f"net:{t.get('network_id')}" for t in r["target_devices"])


@pytest.fixture
def unifi():
    fake = FakeUnifi()

    async def _req(self, method, path, json=None):
        return await fake.request(self, method, path, json)

    with patch.object(router_mod.UnifiAdapter, "_request", _req):
        yield fake


@pytest.fixture
def ping():
    state = {"up": True}

    async def _ping(self, host, count, timeout=2):
        return PingResult(host, state["up"], 12.3 if state["up"] else None, 0.0 if state["up"] else 100.0)

    with patch("custom_components.homelines.monitor.Pinger.ping", _ping):
        yield state


@pytest.fixture(autouse=True)
def no_frontend():
    """Die Testumgebung hat kein gebautes Frontend."""

    async def ok(hass, config):
        return True

    with patch("homeassistant.components.frontend.async_setup", ok), \
            patch("custom_components.homelines.add_extra_js_url"):
        yield
