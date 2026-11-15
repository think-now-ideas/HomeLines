"""Router-Anbindungen: UniFi, Schalter je Gerät, eigene Skripte.

Jede Anbindung liefert eine Geräteliste und setzt um, welche Geräte im
Mobilfunkbetrieb nicht ins Internet dürfen.

Zwei Arten:
* ``persistent``: Die Sperre greift nur, wenn die Hauptleitung ausfällt
  (UniFi-Regel mit Kill Switch). Sie bleibt deshalb dauerhaft gesetzt und
  schützt sofort, auch wenn Home Assistant gerade hängt.
* nicht persistent: Die Sperre wirkt immer (FRITZ!Box-Schalter, Skripte).
  Sie wird erst im Notbetrieb gesetzt und danach wieder aufgehoben.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json as _json
import logging
import time
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CLIENT_MAX_AGE_DAYS,
    CONF_API_KEY,
    CONF_HOST,
    CONF_PRIMARY_WAN_NET,
    CONF_SCRIPT_BLOCK,
    CONF_SCRIPT_UNBLOCK,
    CONF_SITE,
    CONF_SWITCH_ENTITIES,
    CONF_TRACKER_ENTITIES,
    CONF_VERIFY_SSL,
    EVENT_BLOCK,
    ROUTER_SCRIPTS,
    ROUTER_SWITCHES,
    ROUTER_UNIFI,
)

_LOGGER = logging.getLogger(__name__)

ROUTE_DESCRIPTION = "HomeLines Notbetrieb"


def _api_message(text: str) -> str:
    """Aus der UniFi-Antwort nur die Fehlerkennung, nicht das ganze JSON."""
    try:
        data = _json.loads(text)
        meta = data.get("meta", {}) if isinstance(data, dict) else {}
        msg = meta.get("msg") or (data.get("errorCode") if isinstance(data, dict) else None) \
            or (data.get("message") if isinstance(data, dict) else None)
        if msg:
            return str(msg)
    except ValueError:
        pass
    return text[:200]


class RouterError(Exception):
    """Fehler bei der Kommunikation mit dem Router."""


class RouterAuthError(RouterError):
    """Zugangsdaten abgelehnt."""


@dataclass
class Device:
    """Ein Gerät im Netz."""

    id: str  # MAC oder Entity-ID
    name: str
    network_id: str | None = None
    online: bool = False
    ip: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "network_id": self.network_id,
                "online": self.online, "ip": self.ip}


@dataclass
class Network:
    """Ein (LAN-)Netz oder eine WAN-Leitung."""

    id: str
    name: str
    wan_group: str | None = None  # z. B. WAN2


@dataclass
class Inventory:
    devices: list[Device] = field(default_factory=list)
    networks: list[Network] = field(default_factory=list)
    wans: list[Network] = field(default_factory=list)


class BaseAdapter:
    """Gemeinsame Schnittstelle. Andere Router können hier andocken."""

    persistent = False
    supports_networks = False

    def __init__(self, hass: HomeAssistant, config: dict[str, Any]) -> None:
        self.hass = hass
        self.config = config
        self.last_error: str | None = None

    async def async_test(self) -> Inventory:
        return await self.async_inventory()

    async def async_inventory(self) -> Inventory:
        return Inventory()

    async def async_apply(self, blocked_devices: list[str], blocked_networks: list[str],
                          active: bool) -> None:
        """Sperre setzen.

        ``active`` ist True, wenn gerade über die Backup-Leitung gearbeitet wird.
        Persistente Anbindungen ignorieren das und setzen die Sperre immer.
        """


class NoneAdapter(BaseAdapter):
    """Keine Sperre, nur Überwachung und Timer."""


class UnifiAdapter(BaseAdapter):
    """UniFi Network über den lokalen API-Schlüssel."""

    persistent = True
    supports_networks = True

    def __init__(self, hass: HomeAssistant, config: dict[str, Any]) -> None:
        super().__init__(hass, config)
        host = config[CONF_HOST].strip().rstrip("/")
        if not host.startswith("http"):
            host = f"https://{host}"
        self._base = host
        self._site = config.get(CONF_SITE) or "default"
        self._session = async_get_clientsession(hass, verify_ssl=config.get(CONF_VERIFY_SSL, False))
        self._route_id: str | None = None
        self._last_payload: tuple | None = None
        # Vom Hub abgeglichene ID der Hauptleitung (kann von der gespeicherten abweichen,
        # wenn UniFi die WAN-Konfiguration neu angelegt hat).
        self.wan_net: str | None = None

    async def _request(self, method: str, path: str, json: Any = None) -> Any:
        url = f"{self._base}/proxy/network{path}"
        headers = {"X-API-KEY": self.config[CONF_API_KEY], "Accept": "application/json"}
        try:
            async with self._session.request(method, url, json=json, headers=headers,
                                             timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status in (401, 403):
                    raise RouterAuthError(f"HTTP {resp.status}")
                text = await resp.text()
                if resp.status >= 400:
                    raise RouterError(f"HTTP {resp.status}: {_api_message(text)}")
                if not text:
                    return None
                data = await resp.json(content_type=None)
        except (aiohttp.ClientError, TimeoutError) as err:
            raise RouterError(str(err)) from err
        if isinstance(data, dict) and "data" in data and "meta" in data:
            return data["data"]
        return data

    async def async_inventory(self) -> Inventory:
        inv = Inventory()
        nets = await self._request("GET", f"/api/s/{self._site}/rest/networkconf") or []
        for n in nets:
            if n.get("purpose") == "wan":
                inv.wans.append(Network(n["_id"], n.get("name") or n.get("wan_networkgroup", "WAN"),
                                        n.get("wan_networkgroup")))
            elif n.get("purpose") in ("corporate", "guest", "vlan-only"):
                inv.networks.append(Network(n["_id"], n.get("name", n["_id"])))
        net_by_name = {n.name: n.id for n in inv.networks}

        online: dict[str, dict] = {}
        for c in await self._request("GET", f"/api/s/{self._site}/stat/sta") or []:
            if c.get("mac"):
                online[c["mac"].lower()] = c
        known = await self._request("GET", f"/api/s/{self._site}/rest/user") or []
        cutoff = time.time() - CLIENT_MAX_AGE_DAYS * 86400
        seen: set[str] = set()
        for c in [*online.values(), *known]:
            mac = (c.get("mac") or "").lower()
            if not mac or mac in seen:
                continue
            live = online.get(mac)
            if not live and (c.get("last_seen") or 0) < cutoff:
                continue
            seen.add(mac)
            src = live or c
            name = c.get("name") or src.get("name") or src.get("hostname") or mac
            net_id = src.get("network_id") or net_by_name.get(src.get("network", ""))
            inv.devices.append(Device(mac, name, net_id, bool(live), src.get("ip")))
        inv.devices.sort(key=lambda d: d.name.lower())
        return inv

    async def _find_route(self) -> dict | None:
        routes = await self._request("GET", f"/v2/api/site/{self._site}/trafficroutes") or []
        for r in routes:
            if r.get("_id") == self._route_id or r.get("description") == ROUTE_DESCRIPTION:
                self._route_id = r.get("_id")
                return r
        return None

    async def async_apply(self, blocked_devices: list[str], blocked_networks: list[str],
                          active: bool) -> None:
        wan_net = self.wan_net or self.config.get(CONF_PRIMARY_WAN_NET)
        if not wan_net:
            raise RouterError("Keine Hauptleitung für die Regel gewählt")
        targets: list[dict] = [{"network_id": n, "type": "NETWORK"} for n in sorted(blocked_networks)]
        targets += [{"client_mac": m, "type": "CLIENT"} for m in sorted(blocked_devices)]
        key = (wan_net, tuple(sorted(blocked_networks)), tuple(sorted(blocked_devices)))
        if key == self._last_payload and self._route_id:
            return
        existing = await self._find_route()
        enabled = bool(targets)
        body = dict(existing or {})
        body.update({
            "description": ROUTE_DESCRIPTION,
            "enabled": enabled,
            "kill_switch_enabled": True,
            "matching_target": "INTERNET",
            "network_id": wan_net,
            "next_hop": "",
            "target_devices": targets or [{"type": "ALL_CLIENTS"}],
            "domains": [],
            "ip_addresses": [],
            "ip_ranges": [],
            "regions": [],
        })
        if existing:
            await self._request("PUT", f"/v2/api/site/{self._site}/trafficroutes/{existing['_id']}", body)
        elif enabled:
            body.pop("_id", None)
            res = await self._request("POST", f"/v2/api/site/{self._site}/trafficroutes", body)
            if isinstance(res, dict):
                self._route_id = res.get("_id")
        self._last_payload = key
        _LOGGER.debug("UniFi-Regel gesetzt: %s Netze, %s Geräte, aktiv=%s",
                      len(blocked_networks), len(blocked_devices), enabled)

    async def async_remove(self) -> None:
        existing = await self._find_route()
        if existing:
            await self._request("DELETE", f"/v2/api/site/{self._site}/trafficroutes/{existing['_id']}")

    async def async_remove_route(self, description: str) -> int:
        """Fremde bzw. alte Regel mit dieser Beschreibung löschen (z. B. vom Vorgänger)."""
        removed = 0
        for r in await self._request("GET", f"/v2/api/site/{self._site}/trafficroutes") or []:
            if r.get("description") == description and r.get("_id"):
                await self._request("DELETE", f"/v2/api/site/{self._site}/trafficroutes/{r['_id']}")
                removed += 1
        return removed


class SwitchAdapter(BaseAdapter):
    """Ein HA-Schalter je Gerät (an = Internet erlaubt), z. B. FRITZ!Box."""

    async def async_inventory(self) -> Inventory:
        inv = Inventory()
        for ent in self.config.get(CONF_SWITCH_ENTITIES, []):
            st = self.hass.states.get(ent)
            name = st.name if st else ent
            inv.devices.append(Device(ent, name, None, bool(st and st.state != "unavailable")))
        return inv

    async def async_apply(self, blocked_devices: list[str], blocked_networks: list[str],
                          active: bool) -> None:
        blocked = set(blocked_devices) if active else set()
        for ent in self.config.get(CONF_SWITCH_ENTITIES, []):
            st = self.hass.states.get(ent)
            want_on = ent not in blocked
            if st is None or st.state == ("on" if want_on else "off"):
                continue
            await self.hass.services.async_call(
                "switch", "turn_on" if want_on else "turn_off", {"entity_id": ent}, blocking=True)


class ScriptAdapter(BaseAdapter):
    """Eigene Skripte: bekommen die Geräteliste als Variable ``devices``."""

    async def async_inventory(self) -> Inventory:
        inv = Inventory()
        for ent in self.config.get(CONF_TRACKER_ENTITIES, []):
            st = self.hass.states.get(ent)
            name = st.name if st else ent
            inv.devices.append(Device(ent, name, None, bool(st and st.state == "home"),
                                      st.attributes.get("ip") if st else None))
        return inv

    async def async_apply(self, blocked_devices: list[str], blocked_networks: list[str],
                          active: bool) -> None:
        devices = sorted(blocked_devices) if active else []
        macs = []
        for ent in devices:
            st = self.hass.states.get(ent)
            macs.append((st.attributes.get("mac") if st else None) or ent)
        self.hass.bus.async_fire(EVENT_BLOCK, {"active": active, "devices": devices, "macs": macs})
        script = self.config.get(CONF_SCRIPT_BLOCK if active else CONF_SCRIPT_UNBLOCK)
        if script:
            await self.hass.services.async_call(
                "script", "turn_on",
                {"entity_id": script, "variables": {"devices": devices, "macs": macs}},
                blocking=False)


def create_adapter(hass: HomeAssistant, router_type: str, config: dict[str, Any]) -> BaseAdapter:
    if router_type == ROUTER_UNIFI:
        return UnifiAdapter(hass, config)
    if router_type == ROUTER_SWITCHES:
        return SwitchAdapter(hass, config)
    if router_type == ROUTER_SCRIPTS:
        return ScriptAdapter(hass, config)
    return NoneAdapter(hass, config)
