"""HomeLines-Hub: Überwachung, Notbetrieb, Kosten, Neueinwahl und Gerätegruppen."""

from __future__ import annotations

import asyncio
from datetime import datetime, time as dtime, timedelta
import logging
import re
from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr, entity_registry as er, issue_registry as ir
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import (
    async_call_later,
    async_track_point_in_utc_time,
    async_track_state_change_event,
    async_track_time_change,
    async_track_time_interval,
)
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .const import (
    CONF_ACTIVE_WAN_ENTITY,
    CONF_BACKUP_WAN,
    CONF_BOOKING_URL,
    CONF_BUFFER_MIN,
    CONF_DAYFLAT_HOURS,
    CONF_DAYFLAT_PRICE,
    CONF_DEFAULT_GROUP,
    CONF_EMERGENCY_INTERVAL,
    CONF_FAILURES,
    CONF_INCLUDED_MB,
    CONF_INTERVAL,
    CONF_BACKUP_DOWN_MIN,
    CONF_CUSTOM_DOWN_ENTITY,
    CONF_DETECT_DELAY,
    CONF_DETECTION,
    CONF_PHONE_WIFI,
    CONF_PRIMARY_STATUS_ENTITY,
    CONF_RECONNECT_ENTITY,
    CONF_STANDBY,
    CONF_WAN_IP_ENTITY,
    DEFAULT_DELAY_COLD,
    DEFAULT_DELAY_WARM,
    DETECT_ACTIVE_WAN,
    DETECT_CUSTOM,
    DETECT_MONITOR,
    DETECT_PRIMARY_OFF,
    METHOD_HA_ACTION,
    RECONNECT_POLL,
    RECONNECT_WAIT,
    RESULT_NO_EFFECT,
    RESULT_TRIGGERED,
    SSH_METHODS,
    STANDBY_COLD,
    STANDBY_WARM,
    CONF_NOTIFY,
    CONF_NOTIFY_ROUTES,
    CONF_NOTIFY_TARGETS,
    DEFAULT_BACKUP_DOWN_MIN,
    MESSAGES,
    MSG_BACKUP_DOWN,
    MSG_EMERGENCY,
    MSG_FLAT_EXPIRED,
    MSG_FLAT_WARNING,
    MSG_PHONE_SILENT,
    MSG_RECONNECT_FAILED,
    MSG_RESTORED,
    CONF_PHONE_BATTERY,
    CONF_PHONE_CHARGER,
    CONF_PHONE_MOBILE_DATA,
    CONF_PHONE_NETWORK,
    CONF_PHONE_OPERATOR,
    CONF_PHONE_RX,
    CONF_PHONE_SIGNAL,
    CONF_PHONE_STALE_MIN,
    CONF_PHONE_NOTIFY,
    CONF_PHONE_WAKE_MIN,
    DEFAULT_PHONE_WAKE_MIN,
    WAKE_MESSAGE,
    CONF_PHONE_TX,
    CONF_PING_COUNT,
    CONF_PPP_INTERFACE,
    CONF_PRICE_PER_MB,
    CONF_PROVIDER,
    CONF_RECONNECT_ENABLED,
    CONF_RECONNECT_METHOD,
    CONF_RECONNECT_TIME,
    CONF_ROUTER_IP,
    CONF_ROUTER_TYPE,
    CONF_SPEEDTEST_SWITCH,
    CONF_SSH_HOST,
    CONF_SSH_PASSWORD,
    CONF_SSH_PORT,
    CONF_IMPORTED_FROM,
    CONF_PRIMARY_WAN_LABEL,
    CONF_PRIMARY_WAN_NET,
    CONF_SSH_USER,
    CONF_START_BALANCE,
    CONF_TARGETS,
    CONF_WAN_STATUS_ENTITIES,
    DEFAULT_BUFFER_MIN,
    DEFAULT_DAYFLAT_HOURS,
    DEFAULT_DAYFLAT_PRICE,
    DEFAULT_EMERGENCY_INTERVAL,
    DEFAULT_FAILURES,
    DEFAULT_GROUP,
    DEFAULT_INCLUDED_MB,
    DEFAULT_INTERVAL,
    DEFAULT_PHONE_STALE_MIN,
    DEFAULT_PING_COUNT,
    DEFAULT_PPP_INTERFACE,
    DEFAULT_PRICE_PER_MB,
    DEFAULT_PROVIDER,
    DEFAULT_RECONNECT_TIME,
    DEFAULT_SSH_PORT,
    DEFAULT_SSH_USER,
    DEFAULT_START_BALANCE,
    DEFAULT_TARGETS,
    DOMAIN,
    EVENT_MODE_CHANGED,
    EVENT_OUTAGE_ENDED,
    EVENT_OUTAGE_STARTED,
    EVENT_RECONNECTED,
    ISSUE_LEGACY,
    CONF_BACKUP_EXTRA,
    CONF_SPEED_DOWN,
    CONF_SPEED_EXTRA,
    CONF_MONITOR_EXTRA,
    CONF_SPEED_UP,
    LINE_DETAIL_KEYS,
    LINE_HISTORY_KEYS,
    LINE_NAME_KEYS,
    ISSUE_WAN,
    LEGACY_DOMAIN,
    LEGACY_ROUTE_DESCRIPTION,
    GROUP_ALWAYS,
    GROUP_DAYFLAT,
    GROUP_NEVER,
    GROUPS,
    METHOD_PPPD_HUP,
    MODE_DAYFLAT,
    MODE_EMERGENCY,
    MODE_NORMAL,
    PHONE_KEYS,
    RECONNECT_GRACE,
    RESULT_ERROR,
    RESULT_NEW_IP,
    RESULT_SAME_IP,
    ROUTER_NONE,
    SIGNAL_UPDATE,
    STORAGE_VERSION,
)
from .monitor import CAUSE_INTERNET, CAUSE_LOCAL, CAUSE_UNKNOWN, OutageLog, Pinger, fmt_duration
from .reconnect import SSHClient, SSHError
from .router import BaseAdapter, Inventory, RouterError, create_adapter

_LOGGER = logging.getLogger(__name__)

# "WAN3", "wan3_internet", "WAN 2 (Port 3)" – aber nicht "wan_192_168_1" aus einer IP im Namen
_WAN_RE = re.compile(r"wan ?(\d{1,2})(?!\d)", re.IGNORECASE)
INVENTORY_INTERVAL = timedelta(minutes=5)
EXPIRY_WARNING = timedelta(minutes=15)


class FlatError(Exception):
    """Freischaltung nicht möglich. args[0] ist ein Übersetzungsschlüssel."""


def _wan_id(text: str | None) -> str | None:
    if not text:
        return None
    found = _WAN_RE.findall(text)
    if found:
        return f"WAN{found[-1]}"
    if text.strip().upper() == "WAN":
        return "WAN1"
    return None


def _float(state) -> float | None:
    if state is None or state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN, ""):
        return None
    try:
        return float(state.state)
    except (TypeError, ValueError):
        return None


class HomeLinesHub:
    """Hält den gesamten Zustand einer HomeLines-Instanz."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._store = Store(hass, STORAGE_VERSION, f"{DOMAIN}.{entry.entry_id}")
        self.data: dict[str, Any] = {}
        self.log = OutageLog()
        self.pinger = Pinger()
        self.adapter: BaseAdapter = create_adapter(hass, self.conf.get(CONF_ROUTER_TYPE, ROUTER_NONE), self.conf)
        self.inventory = Inventory()
        self.router_error: str | None = None
        self._unsubs: list[CALLBACK_TYPE] = []
        self._ping_unsub: CALLBACK_TYPE | None = None
        self._restore_unsub: CALLBACK_TYPE | None = None
        self._warn_unsub: CALLBACK_TYPE | None = None
        self._planned_until: datetime | None = None
        self._failures = 0
        self.internet: bool | None = None
        self.router_ok: bool | None = None
        self.latency: float | None = None
        self.last_check: datetime | None = None
        self.loss: float | None = None
        self.reconnect_running = False
        self._apply_lock = asyncio.Lock()
        self._down_since: datetime | None = None
        self._down_unsub: CALLBACK_TYPE | None = None
        self.wan_missing: str | None = None  # Name der Hauptleitung, wenn UniFi sie nicht mehr kennt
        self.missing_networks: list[dict] = []

    # ------------------------------------------------------------------ Konfig
    @property
    def conf(self) -> dict[str, Any]:
        return {**self.entry.data, **self.entry.options}

    @property
    def router_ip(self) -> str | None:
        ip = self.conf.get(CONF_ROUTER_IP)
        if ip:
            return ip
        host = self.conf.get("host")
        if host and self.conf.get(CONF_ROUTER_TYPE) == "unifi":
            from urllib.parse import urlparse
            return urlparse(host if "://" in host else f"//{host}").hostname
        return None

    def opt(self, key: str, default: Any = None) -> Any:
        val = self.conf.get(key)
        return default if val in (None, "") else val

    @property
    def mode(self) -> str:
        return self.data["mode"]["mode"]

    # ------------------------------------------------------------------ Start
    async def async_start(self) -> None:
        stored = await self._store.async_load() or {}
        if not stored and self.conf.get(CONF_IMPORTED_FROM):
            stored = await self._load_legacy(self.conf[CONF_IMPORTED_FROM])
        self.data = {
            "mode": {"mode": MODE_NORMAL, "since": None, "booked_at": None, "flat_end": None,
                     "restore_at": None, "notified": False, "speedtest_was_on": None},
            "groups": {"devices": {}, "networks": {}},
            "usage": {"reset_at": dt_util.utcnow().isoformat(), "mb": 0.0, "cost": 0.0,
                      "last_total": None, "flats": 0, "start_balance": None},
            "reconnect": {"enabled": None, "time": None, "last": None, "result": None,
                          "ip": None, "old_ip": None},
            "history": {"emergencies": []},
            "ids": {"wan": None, "networks": {}},
            **{k: v for k, v in stored.items() if k != "outages"},
        }
        if stored.get("legacy", {}).get("fresh"):
            del self.data["legacy"]["fresh"]
            await self._store.async_save(self._stored())
        self.log = OutageLog(stored.get("outages"))
        if self.log.current:
            # Ausfall lief über einen Neustart: mit letztem Offline-Zeitpunkt abschließen.
            self.log.end(dt_util.utcnow(), interrupted=True)

        self._track_entities()
        sources = [self.opt(CONF_PHONE_RX), self.opt(CONF_PHONE_TX)]
        if self.data["usage"].get("last_total") is None or self.data["usage"].get("sources") != sources:
            # Neue oder geänderte Zähler: nur den Startwert merken, nichts als Verbrauch werten
            self.data["usage"]["last_total"] = self._phone_total_mb()
            self.data["usage"]["sources"] = sources
        self._unsubs.append(async_track_time_interval(self.hass, self._async_refresh_inventory,
                                                      INVENTORY_INTERVAL))
        self._unsubs.append(async_track_time_interval(self.hass, self._async_watch, timedelta(minutes=1)))
        self._schedule_reconnect()
        self._reschedule_ping()
        self._reschedule_flat()
        self.hass.async_create_task(self._async_refresh_inventory())
        self.hass.async_create_task(self._async_ping())
        self.hass.async_create_task(self._async_check_wan())

    async def _load_legacy(self, old_entry_id: str) -> dict:
        """Einmalig: Gruppen, Zähler, Tarif-Stand und Ausfallhistorie vom Vorgänger LineGuard übernehmen."""
        old = await Store(self.hass, STORAGE_VERSION, f"{LEGACY_DOMAIN}.{old_entry_id}").async_load() or {}
        old.pop("ids_fixed", None)
        _LOGGER.info("Daten von LineGuard übernommen (%s Einträge)", len(old))
        return {**old, "legacy": {"route_removed": False, "fresh": True}}

    async def _cleanup_legacy(self) -> None:
        """Nach der Übernahme: Hinweis, solange LineGuard noch läuft, danach dessen UniFi-Regel löschen."""
        leg = self.data.get("legacy")
        if not leg:
            return
        old_id = self.conf.get(CONF_IMPORTED_FROM)
        old = self.hass.config_entries.async_get_entry(old_id) if old_id else None
        issue = f"{ISSUE_LEGACY}_{self.entry.entry_id}"
        if old is not None and old.domain == LEGACY_DOMAIN and old.state is ConfigEntryState.LOADED:
            ir.async_create_issue(self.hass, DOMAIN, issue, is_fixable=False, severity=ir.IssueSeverity.WARNING,
                                  translation_key=ISSUE_LEGACY)
            return
        ir.async_delete_issue(self.hass, DOMAIN, issue)
        if leg.get("route_removed"):
            return
        remove = getattr(self.adapter, "async_remove_route", None)
        if remove:
            try:
                if await remove(LEGACY_ROUTE_DESCRIPTION):
                    _LOGGER.info("Alte UniFi-Regel „%s“ entfernt", LEGACY_ROUTE_DESCRIPTION)
            except RouterError as err:
                _LOGGER.debug("Alte Regel noch nicht entfernt: %s", err)
                return
        leg["route_removed"] = True
        self._save()

    # -------------------------------------------------------- IDs abgleichen
    def _reconcile_ids(self) -> None:
        """UniFi vergibt beim Neuanlegen einer WAN- oder Netzkonfiguration neue IDs.

        Neben der ID merkt sich HomeLines Name und WAN-Gruppe. Fehlt eine ID, wird über
        Gruppe bzw. Namen die neue gesucht und still übernommen. Lässt sich nichts zuordnen,
        gibt es einen klaren Hinweis statt einer Fehlermeldung des Routers.
        """
        if not self.adapter.supports_networks:
            return
        ids = self.data.setdefault("ids", {"wan": None, "networks": {}})
        changed = False
        inv = self.inventory

        # Hauptleitung
        conf_id = self.opt(CONF_PRIMARY_WAN_NET)
        wans = {w.id: w for w in inv.wans}
        rec = ids.get("wan")
        if conf_id and (not rec or rec.get("conf") != conf_id):
            w = wans.get(conf_id)
            label = self.opt(CONF_PRIMARY_WAN_LABEL) or {}
            rec = {"conf": conf_id, "id": conf_id, "name": w.name if w else label.get("name"),
                   "group": w.wan_group if w else label.get("group")}
            changed = True
        if rec and wans:
            w = wans.get(rec["id"])
            if w is None:
                w = (next((x for x in wans.values() if rec.get("group") and x.wan_group == rec["group"]), None)
                     or next((x for x in wans.values() if rec.get("name") and x.name == rec["name"]), None))
                if w is not None:
                    _LOGGER.info("Hauptleitung „%s“ hat in UniFi eine neue ID – übernommen", w.name)
            if w is not None:
                if (rec["id"], rec.get("name"), rec.get("group")) != (w.id, w.name, w.wan_group):
                    rec.update(id=w.id, name=w.name, group=w.wan_group)
                    changed = True
                self.wan_missing = None
            else:
                self.wan_missing = rec.get("name") or rec.get("group") or rec["id"]
        ids["wan"] = rec
        if hasattr(self.adapter, "wan_net"):
            self.adapter.wan_net = rec["id"] if rec and not self.wan_missing else None

        # Netze mit eigener Gruppe
        nets = {n.id: n for n in inv.networks}
        names: dict = ids.setdefault("networks", {})
        groups = self.data["groups"]["networks"]
        if nets:
            for nid in list(groups):
                if nid in nets:
                    if names.get(nid) != nets[nid].name:
                        names[nid] = nets[nid].name
                        changed = True
                    continue
                old_name = names.get(nid)
                match = next((n for n in nets.values() if old_name and n.name == old_name and n.id not in groups), None)
                if match:
                    _LOGGER.info("Netz „%s“ hat in UniFi eine neue ID – Gruppe übernommen", match.name)
                    groups[match.id] = groups.pop(nid)
                    names[match.id] = match.name
                    names.pop(nid, None)
                    changed = True
            self.missing_networks = [{"id": nid, "name": names.get(nid) or nid, "group": g, "missing": True}
                                     for nid, g in groups.items() if nid not in nets]
        if changed:
            self._save()

    def _router_message(self, err: Exception | str) -> str:
        if self.wan_missing:
            return (f"Hauptleitung „{self.wan_missing}“ in UniFi nicht mehr gefunden (vermutlich neu angelegt) – "
                    "bitte unter HomeLines → Konfigurieren → Leitungen neu wählen.")
        return str(err)

    def _update_wan_issue(self) -> None:
        issue = f"{ISSUE_WAN}_{self.entry.entry_id}"
        if self.wan_missing:
            ir.async_create_issue(self.hass, DOMAIN, issue, is_fixable=False, severity=ir.IssueSeverity.ERROR,
                                  translation_key=ISSUE_WAN, translation_placeholders={"name": self.wan_missing})
        else:
            ir.async_delete_issue(self.hass, DOMAIN, issue)

    async def async_stop(self) -> None:
        for u in self._unsubs:
            u()
        self._unsubs.clear()
        for attr in ("_ping_unsub", "_restore_unsub", "_warn_unsub"):
            if (u := getattr(self, attr)) is not None:
                u()
                setattr(self, attr, None)
        await self._store.async_save(self._stored())

    def _stored(self) -> dict:
        return {**self.data, "outages": self.log.as_dict()}

    def _save(self) -> None:
        self._store.async_delay_save(self._stored, 5)

    @callback
    def _push(self) -> None:
        async_dispatcher_send(self.hass, SIGNAL_UPDATE.format(self.entry.entry_id))

    def _track_entities(self) -> None:
        wan_ents = [e for e in [self.opt(CONF_ACTIVE_WAN_ENTITY), self.opt(CONF_PRIMARY_STATUS_ENTITY),
                                self.opt(CONF_CUSTOM_DOWN_ENTITY), *self.opt(CONF_WAN_STATUS_ENTITIES, [])] if e]
        if wan_ents:
            self._unsubs.append(async_track_state_change_event(self.hass, wan_ents, self._on_wan_event))
        usage_ents = [e for e in (self.opt(CONF_PHONE_RX), self.opt(CONF_PHONE_TX)) if e]
        if usage_ents:
            self._unsubs.append(async_track_state_change_event(self.hass, usage_ents, self._on_usage_event))
        phone = [self.opt(k) for k in PHONE_KEYS if self.opt(k) and k not in (CONF_PHONE_RX, CONF_PHONE_TX)]
        if phone:
            self._unsubs.append(async_track_state_change_event(self.hass, phone, self._on_phone_event))

    # ------------------------------------------------------------- Monitor
    def _reschedule_ping(self) -> None:
        if self._ping_unsub:
            self._ping_unsub()
        secs = self.opt(CONF_INTERVAL, DEFAULT_INTERVAL)
        if self.mode != MODE_NORMAL:
            secs = max(secs, self.opt(CONF_EMERGENCY_INTERVAL, DEFAULT_EMERGENCY_INTERVAL))
        self._ping_unsub = async_track_time_interval(self.hass, self._async_ping, timedelta(seconds=secs))

    async def _async_ping(self, _now=None) -> None:
        targets = [t.strip() for t in str(self.opt(CONF_TARGETS, DEFAULT_TARGETS)).split(",") if t.strip()]
        count = int(self.opt(CONF_PING_COUNT, DEFAULT_PING_COUNT))
        results = await asyncio.gather(*(self.pinger.ping(t, count) for t in targets))
        ok = [r for r in results if r.reachable]
        lat = [r.latency for r in ok if r.latency is not None]
        self.last_check = dt_util.utcnow()
        self.latency = round(min(lat), 1) if lat else None
        self.loss = round(min(r.loss for r in results), 1) if results else None
        now = dt_util.utcnow()
        router_ip = self.router_ip
        if ok:
            self._failures = 0
            if self.internet is False or self.log.current:
                entry = self.log.end(now)
                if entry:
                    self.hass.bus.async_fire(EVENT_OUTAGE_ENDED, {
                        **entry, "duration_text": fmt_duration(entry["duration"])})
                    self._save()
            self.internet = True
            if router_ip:
                self.router_ok = True
        else:
            self._failures += 1
            cause = CAUSE_UNKNOWN
            if router_ip:
                r = await self.pinger.ping(router_ip, 2)
                self.router_ok = r.reachable
                cause = CAUSE_INTERNET if r.reachable else CAUSE_LOCAL
            if self._failures >= int(self.opt(CONF_FAILURES, DEFAULT_FAILURES)):
                if self.log.current is None:
                    self.log.start(now, cause)
                    self.hass.bus.async_fire(EVENT_OUTAGE_STARTED, {"start": now.isoformat(), "cause": cause})
                else:
                    self.log.touch(now, cause)
                self.internet = False
                self._save()
        if self.detection == DETECT_MONITOR:
            await self._async_check_wan()
        self._push()

    # ------------------------------------------------------------- Leitungen
    def wan_lines(self) -> list[dict]:
        active = self.active_wan()
        names = {(_wan_id(w.wan_group) or w.wan_group): w.name for w in self.inventory.wans if w.wan_group}
        custom = self.line_names()
        lines: dict[str, dict] = {}
        for ent in self.opt(CONF_WAN_STATUS_ENTITIES, []):
            st = self.hass.states.get(ent)
            wid = _wan_id(ent) or _wan_id(st.name if st else None) or ent
            state = "unavailable" if st is None or st.state == STATE_UNAVAILABLE else (
                "online" if st.state == "on" else "offline")
            lines[wid] = {"id": wid, "name": names.get(wid, st.name if st else wid), "state": state,
                          "entity_id": ent}
        for wid, name in names.items():
            lines.setdefault(wid, {"id": wid, "name": name, "state": "unknown", "entity_id": None})
        for wid, name in custom.items():
            lines.setdefault(wid, {"id": wid, "name": name, "state": "unknown", "entity_id": None})
        primary = self.primary_wan()
        for line in lines.values():
            if line["id"] in custom:
                line["name"] = custom[line["id"]]
            line["active"] = line["id"] == active
            line["primary"] = line["id"] == primary
            line["backup"] = line["id"] == self.backup_wan()
            if line["active"] and line["state"] == "unknown":
                line["state"] = "online"
        return sorted(lines.values(), key=lambda l: l["id"])

    def primary_wan(self) -> str | None:
        """Hauptleitung (z. B. WAN2): aus der UniFi-Zuordnung, sonst aus dem Status-Sensor."""
        rec = (self.data.get("ids") or {}).get("wan") or {}
        wid = _wan_id(rec.get("group")) if rec.get("group") else None
        wid = wid or _wan_id(self.opt(CONF_PRIMARY_STATUS_ENTITY))
        if wid:
            return wid
        # Ohne UniFi-Zuordnung und Status-Sensor: die erste Leitung mit Status-Sensor, die nicht Backup ist
        backup = self.backup_wan()
        for ent in self.opt(CONF_WAN_STATUS_ENTITIES, []):
            st = self.hass.states.get(ent)
            cand = _wan_id(ent) or _wan_id(st.name if st else None)
            if cand and cand != backup:
                return cand
        return None

    def details(self) -> dict:
        """Was die Detailfenster der Karte zeigen (nur Entitäts-IDs, die Werte holt die Karte selbst)."""
        reg = er.async_get(self.hass)
        prefix = f"{self.entry.entry_id}_"
        own = {e.unique_id[len(prefix):]: e.entity_id
               for e in er.async_entries_for_config_entry(reg, self.entry.entry_id) if e.unique_id.startswith(prefix)}
        lines = {}
        for (dk, wid), hk in zip(LINE_DETAIL_KEYS.items(), LINE_HISTORY_KEYS):
            ents, hist = list(self.opt(dk, []) or []), list(self.opt(hk, []) or [])
            if ents or hist:
                lines[wid] = {"entities": ents, "history": hist}
        phone = [self.opt(k) for k in (CONF_PHONE_BATTERY, CONF_PHONE_SIGNAL, CONF_PHONE_NETWORK,
                                        CONF_PHONE_MOBILE_DATA, CONF_PHONE_CHARGER) if self.opt(k)]
        return {"lines": lines, "speed": {"download": self.opt(CONF_SPEED_DOWN), "upload": self.opt(CONF_SPEED_UP),
                          "extra": list(self.opt(CONF_SPEED_EXTRA, []) or [])},
                "backup": list(self.opt(CONF_BACKUP_EXTRA, []) or []), "phone": phone, "own": own,
                "monitor": list(self.opt(CONF_MONITOR_EXTRA, []) or []),
                "active_wan_entity": self.opt(CONF_ACTIVE_WAN_ENTITY)}

    def line_names(self) -> dict[str, str]:
        """Eigene Namen aus den Optionen, z. B. {"WAN2": "DSL"}."""
        return {wid: str(self.opt(key)).strip() for key, wid in LINE_NAME_KEYS.items()
                if str(self.opt(key) or "").strip()}

    def line_name(self, wid: str | None) -> str | None:
        if not wid:
            return None
        return next((l["name"] for l in self.wan_lines() if l["id"] == wid), wid)

    def active_wan(self) -> str | None:
        st = self.hass.states.get(self.opt(CONF_ACTIVE_WAN_ENTITY) or "")
        if st is None or st.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return None
        return _wan_id(st.state) or st.state

    def backup_wan(self) -> str:
        return _wan_id(self.opt(CONF_BACKUP_WAN, "WAN3")) or str(self.opt(CONF_BACKUP_WAN, "WAN3"))

    @callback
    def _on_wan_event(self, event: Event) -> None:
        self.hass.async_create_task(self._async_check_wan())

    # ------------------------------------------------------------- Erkennung
    @property
    def standby(self) -> str:
        return self.opt(CONF_STANDBY, STANDBY_WARM)

    @property
    def detection(self) -> str:
        return self.opt(CONF_DETECTION, DETECT_ACTIVE_WAN)

    @property
    def detect_delay(self) -> float:
        default = DEFAULT_DELAY_COLD if self.standby == STANDBY_COLD else DEFAULT_DELAY_WARM
        return float(self.opt(CONF_DETECT_DELAY, default))

    def _state(self, key: str):
        ent = self.opt(key)
        return self.hass.states.get(ent) if ent else None

    def backup_running(self) -> bool:
        if self.active_wan() and self.active_wan() == self.backup_wan():
            return True
        if self.standby != STANDBY_COLD or self.mode == MODE_NORMAL:
            return False
        line = next((l for l in self.wan_lines() if l["backup"]), None)
        if line and line["state"] != "unknown":
            return line["state"] == "online"
        # Ohne Status der Backup-Leitung: Handy sieht nach laufendem Tethering aus
        ph = self.phone()
        return bool(ph["mobile_data"] and ph["usb"] and self._phone_wifi() is False)

    def primary_down(self) -> bool | None:
        """True = Hauptleitung weg, False = da, None = unbekannt."""
        prim = self._state(CONF_PRIMARY_STATUS_ENTITY)
        if self.detection == DETECT_CUSTOM:
            st = self._state(CONF_CUSTOM_DOWN_ENTITY)
            return None if st is None or st.state in (STATE_UNAVAILABLE, STATE_UNKNOWN) else st.state == "on"
        if self.detection == DETECT_PRIMARY_OFF:
            if prim is None or prim.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
                return None
            return prim.state == "off"
        if self.detection == DETECT_MONITOR:
            if self.internet is None:
                return None
            if self.mode != MODE_NORMAL and self.internet and self.backup_running():
                return True  # Internet läuft gerade über die Backup-Leitung
            if not self.internet and self.router_ok is False:
                return None  # Heimnetz gestört, nicht die Leitung
            return not self.internet
        active = self.active_wan()
        if prim is not None and prim.state == "off":
            return True
        if active is None:
            return None
        return active == self.backup_wan()

    @callback
    def _on_phone_event(self, event: Event) -> None:
        self._check_return()
        self._push()

    async def _async_check_wan(self, _now=None) -> None:
        down = self.primary_down()
        if down is None:
            self._push()
            return
        if down and self.mode == MODE_NORMAL:
            now = dt_util.utcnow()
            if self._down_since is None:
                self._down_since = now
            waited = (now - self._down_since).total_seconds()
            if waited >= self.detect_delay:
                self._cancel_down_timer()
                await self._enter_emergency()
            elif self._down_unsub is None:
                self._down_unsub = async_call_later(self.hass, self.detect_delay - waited + 0.5,
                                                    self._on_down_timer)
        elif not down:
            self._down_since = None
            self._cancel_down_timer()
            if self.mode != MODE_NORMAL:
                await self._leave_emergency()
        self._push()

    async def _on_down_timer(self, _now=None) -> None:
        self._down_unsub = None
        await self._async_check_wan()

    def _cancel_down_timer(self) -> None:
        if self._down_unsub:
            self._down_unsub()
            self._down_unsub = None

    # ------------------------------------------------------------- Assistent
    def _phone_wifi(self) -> bool | None:
        st = self._state(CONF_PHONE_WIFI)
        if st is None or st.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return None
        return st.state not in ("<not connected>", "off", "disconnected", "")

    def assistant(self) -> dict | None:
        """Schritte für die kalte Bereitschaft: Notfall-Internet ein- oder ausschalten."""
        if self.standby != STANDBY_COLD:
            return None
        ph = self.phone()
        wifi = self._phone_wifi()
        if self.mode != MODE_NORMAL:
            steps = []
            if float(self.opt(CONF_DAYFLAT_PRICE, DEFAULT_DAYFLAT_PRICE)) > 0:
                steps.append({"key": "book", "done": self.mode == MODE_DAYFLAT})
            steps += [
                {"key": "wifi_off", "done": None if wifi is None else not wifi},
                {"key": "data_on", "done": ph["mobile_data"]},
                {"key": "usb", "done": ph["usb"] if ph["charger"] is not None else None},
                {"key": "tether", "done": self.backup_running()},
            ]
            return {"kind": "start", "steps": steps}
        if self.data["mode"].get("return_pending"):
            return {"kind": "return", "steps": [
                {"key": "tether_off", "done": not (self.active_wan() == self.backup_wan())},
                {"key": "data_off", "done": None if ph["mobile_data"] is None else not ph["mobile_data"]},
                {"key": "wifi_on", "done": wifi},
            ]}
        return None

    def _check_return(self) -> None:
        a = self.assistant()
        if a and a["kind"] == "return" and all(s["done"] is not False for s in a["steps"]) \
                and any(s["done"] for s in a["steps"][1:]):
            self.data["mode"]["return_pending"] = False
            self._save()

    async def async_dismiss_return(self) -> None:
        self.data["mode"]["return_pending"] = False
        self._save()
        self._push()

    def _planned(self) -> bool:
        return bool(self._planned_until and dt_util.utcnow() < self._planned_until) or self.reconnect_running

    async def _enter_emergency(self) -> None:
        m = self.data["mode"]
        m.update(mode=MODE_EMERGENCY, since=dt_util.utcnow().isoformat(), booked_at=None,
                 flat_end=None, restore_at=None, notified=False)
        self._fire_mode()
        await self.async_wake_phone("notbetrieb")
        await self._pause_speedtest()
        await self.async_apply_groups()
        self._reschedule_ping()
        if self._planned():
            async_call_later(self.hass, RECONNECT_GRACE, self._late_emergency_notice)
        else:
            await self._notify_emergency()
        self._save()

    async def _late_emergency_notice(self, _now=None) -> None:
        if self.mode != MODE_NORMAL and not self.data["mode"]["notified"]:
            await self._notify_emergency()

    async def _notify_emergency(self) -> None:
        self.data["mode"]["notified"] = True
        allowed = self.counts()["online_now"]
        price = self._eur(self.opt(CONF_DAYFLAT_PRICE, DEFAULT_DAYFLAT_PRICE))
        if self.standby == STANDBY_COLD:
            await self.notify(
                MSG_EMERGENCY, "Internet: Hauptleitung ausgefallen",
                f"Notfall-Internet einschalten: 1. Tagesflat buchen ({price}) und in HomeLines freischalten, "
                "2. am Notfall-Handy WLAN aus und mobile Daten an, 3. USB-Tethering einschalten. "
                "Der Assistent in der HomeLines-Karte zeigt, welcher Schritt fehlt.")
            return
        await self.notify(
            MSG_EMERGENCY, "Internet: Notbetrieb über Mobilfunk",
            f"Die Hauptleitung ist ausgefallen. Nur die Gruppe „Immer“ ist online ({allowed} Geräte). "
            f"Buche bei Bedarf die Tagesflat ({price}) und gib sie in HomeLines frei.")

    async def _leave_emergency(self) -> None:
        m = self.data["mode"]
        since = dt_util.parse_datetime(m["since"]) if m.get("since") else None
        was_notified = m.get("notified")
        if since:
            hist = self.data["history"]["emergencies"]
            hist.append({"start": m["since"], "end": dt_util.utcnow().isoformat(),
                         "flat": m.get("booked_at") is not None})
            self.data["history"]["emergencies"] = hist[-50:]
        m.update(mode=MODE_NORMAL, since=None, booked_at=None, flat_end=None, restore_at=None,
                 notified=False, return_pending=self.standby == STANDBY_COLD and was_notified)
        self._cancel_flat_timers()
        self._fire_mode()
        await self.async_apply_groups()
        await self._resume_speedtest()
        self._reschedule_ping()
        if was_notified:
            dur = fmt_duration((dt_util.utcnow() - since).total_seconds()) if since else "?"
            text = f"Der Notbetrieb ist beendet (Dauer {dur}). Alle Geräte laufen wieder über die Hauptleitung."
            if self.standby == STANDBY_COLD:
                text += (" Bitte das Notfall-Handy zurückstellen: USB-Tethering aus, mobile Daten aus, WLAN an. "
                         "Sonst läuft weiter Datenverkehr über die SIM.")
            await self.notify(MSG_RESTORED, "Internet: Hauptleitung wieder da", text)
        self._save()

    def _fire_mode(self) -> None:
        self.hass.bus.async_fire(EVENT_MODE_CHANGED, {"mode": self.mode, "entry_id": self.entry.entry_id})

    async def _pause_speedtest(self) -> None:
        ent = self.opt(CONF_SPEEDTEST_SWITCH)
        st = self.hass.states.get(ent or "")
        if st is None:
            return
        self.data["mode"]["speedtest_was_on"] = st.state == "on"
        if st.state == "on":
            await self.hass.services.async_call("switch", "turn_off", {"entity_id": ent}, blocking=False)

    async def _resume_speedtest(self) -> None:
        ent = self.opt(CONF_SPEEDTEST_SWITCH)
        if ent and self.data["mode"].get("speedtest_was_on"):
            await self.hass.services.async_call("switch", "turn_on", {"entity_id": ent}, blocking=False)
        self.data["mode"]["speedtest_was_on"] = None

    # ------------------------------------------------------------- Tagesflat
    def flat_preview(self, booked_at: datetime) -> dict:
        flat_end = booked_at + timedelta(hours=float(self.opt(CONF_DAYFLAT_HOURS, DEFAULT_DAYFLAT_HOURS)))
        restore = flat_end - timedelta(minutes=float(self.opt(CONF_BUFFER_MIN, DEFAULT_BUFFER_MIN)))
        return {"booked_at": booked_at.isoformat(), "flat_end": flat_end.isoformat(),
                "restore_at": restore.isoformat()}

    async def async_activate_flat(self, booked_at: datetime | None = None) -> dict:
        if self.mode == MODE_NORMAL:
            raise FlatError("not_in_emergency")
        now = dt_util.utcnow()
        booked_at = dt_util.as_utc(booked_at) if booked_at else now
        if booked_at > now + timedelta(minutes=1):
            raise FlatError("booked_in_future")
        prev = self.flat_preview(booked_at)
        if dt_util.parse_datetime(prev["restore_at"]) <= now:
            raise FlatError("flat_expired")
        m = self.data["mode"]
        new_flat = m.get("booked_at") != prev["booked_at"]
        m.update(mode=MODE_DAYFLAT, **prev)
        if new_flat:
            u = self.data["usage"]
            u["flats"] = u.get("flats", 0) + 1
            u["cost"] = round(u["cost"] + float(self.opt(CONF_DAYFLAT_PRICE, DEFAULT_DAYFLAT_PRICE)), 4)
        self._fire_mode()
        await self.async_apply_groups()
        self._reschedule_flat()
        self._save()
        self._push()
        return prev

    async def async_restrict(self) -> None:
        if self.mode != MODE_DAYFLAT:
            return
        self.data["mode"].update(mode=MODE_EMERGENCY, booked_at=None, flat_end=None, restore_at=None)
        self._cancel_flat_timers()
        self._fire_mode()
        await self.async_apply_groups()
        self._save()
        self._push()

    def _cancel_flat_timers(self) -> None:
        for attr in ("_restore_unsub", "_warn_unsub"):
            if (u := getattr(self, attr)) is not None:
                u()
                setattr(self, attr, None)

    def _reschedule_flat(self) -> None:
        self._cancel_flat_timers()
        m = self.data["mode"]
        if m["mode"] != MODE_DAYFLAT or not m.get("restore_at"):
            return
        restore = dt_util.parse_datetime(m["restore_at"])
        now = dt_util.utcnow()
        if restore <= now:
            self.hass.async_create_task(self._async_flat_expired())
            return
        self._restore_unsub = async_track_point_in_utc_time(self.hass, self._async_flat_expired, restore)
        warn = restore - EXPIRY_WARNING
        if warn > now:
            self._warn_unsub = async_track_point_in_utc_time(self.hass, self._async_flat_warning, warn)

    async def _async_flat_warning(self, _now=None) -> None:
        self._warn_unsub = None
        await self.notify(MSG_FLAT_WARNING, "Internet: Tagesflat endet bald",
                          "In 15 Minuten schaltet HomeLines wieder auf Notbetrieb zurück. "
                          "Buche eine neue Tagesflat, falls die Hauptleitung dann noch fehlt.")

    async def _async_flat_expired(self, _now=None) -> None:
        self._restore_unsub = None
        if self.mode != MODE_DAYFLAT:
            return
        await self.async_restrict()
        await self.notify(MSG_FLAT_EXPIRED, "Internet: zurück im Notbetrieb",
                          "Die Tagesflat-Freigabe ist abgelaufen. Nur die Gruppe „Immer“ ist wieder online.")

    # ------------------------------------------------------------- Gruppen
    def group_of_device(self, dev_id: str, network_id: str | None) -> tuple[str, str]:
        """Effektive Gruppe und woher sie kommt (device / network / default)."""
        g = self.data["groups"]
        if dev_id in g["devices"]:
            return g["devices"][dev_id], "device"
        if network_id and network_id in g["networks"]:
            return g["networks"][network_id], "network"
        return self.opt(CONF_DEFAULT_GROUP, DEFAULT_GROUP), "default"

    def blocked_groups(self) -> set[str]:
        return {GROUP_NEVER} if self.mode == MODE_DAYFLAT else {GROUP_DAYFLAT, GROUP_NEVER}

    def compute_blocked(self) -> tuple[list[str], list[str]]:
        blocked = self.blocked_groups()
        g = self.data["groups"]
        nets: list[str] = []
        if self.adapter.supports_networks:
            for net in self.inventory.networks:
                ng = g["networks"].get(net.id)
                if ng not in blocked:
                    continue
                overrides = [d for d in self.inventory.devices if d.network_id == net.id
                             and g["devices"].get(d.id) not in (None, *blocked)]
                if not overrides:
                    nets.append(net.id)
        devices = [d.id for d in self.inventory.devices if d.network_id not in nets
                   and self.group_of_device(d.id, d.network_id)[0] in blocked]
        return devices, nets

    async def async_set_group(self, kind: str, target_id: str, group: str | None) -> None:
        bucket = self.data["groups"]["networks" if kind == "network" else "devices"]
        if kind == "network":
            names = self.data.setdefault("ids", {"wan": None, "networks": {}}).setdefault("networks", {})
            net = next((n for n in self.inventory.networks if n.id == target_id), None)
            if group is None:
                names.pop(target_id, None)
                self.missing_networks = [n for n in self.missing_networks if n["id"] != target_id]
            elif net:
                names[target_id] = net.name
        if group is None:
            bucket.pop(target_id, None)
        elif group in GROUPS:
            bucket[target_id] = group
        else:
            raise ValueError(group)
        self._save()
        await self.async_apply_groups()
        self._push()

    async def async_apply_groups(self) -> None:
        async with self._apply_lock:
            if self.wan_missing:
                self.router_error = self._router_message("")
                self._update_wan_issue()
                return
            for attempt in (1, 2):
                devices, nets = self.compute_blocked()
                try:
                    await self.adapter.async_apply(devices, nets, self.mode != MODE_NORMAL)
                    self.router_error = None
                    break
                except RouterError as err:
                    if attempt == 1 and "InvalidNetworkConfId" in str(err):
                        # UniFi kennt eine ID nicht mehr: Liste neu holen, abgleichen, noch einmal
                        try:
                            self.inventory = await self.adapter.async_inventory()
                        except RouterError:
                            pass
                        self._reconcile_ids()
                        if not self.wan_missing:
                            continue
                    self.router_error = self._router_message(err)
                    _LOGGER.warning("Router-Regel konnte nicht gesetzt werden: %s", err)
                    break
            self._update_wan_issue()

    async def _async_refresh_inventory(self, _now=None) -> None:
        try:
            self.inventory = await self.adapter.async_inventory()
            self.router_error = None
            self._reconcile_ids()
            await self._protect_self()
            await self._cleanup_legacy()
        except RouterError as err:
            self.router_error = str(err)
            _LOGGER.debug("Geräteliste nicht abrufbar: %s", err)
        await self.async_apply_groups()
        self._push()

    async def _protect_self(self) -> None:
        """Home Assistant selbst immer online lassen, sonst kommen keine Meldungen durch."""
        try:
            from homeassistant.components.network import async_get_source_ip

            own_ip = await async_get_source_ip(self.hass)
        except Exception:  # noqa: BLE001
            return
        groups = self.data["groups"]["devices"]
        for d in self.inventory.devices:
            if d.ip and d.ip == own_ip and d.id not in groups:
                groups[d.id] = GROUP_ALWAYS
                self._save()

    def counts(self) -> dict[str, int]:
        devs = self.inventory.devices
        blocked = self.blocked_groups() if self.mode != MODE_NORMAL else set()
        per_group = {k: 0 for k in GROUPS}
        online_now = 0
        for d in devs:
            grp = self.group_of_device(d.id, d.network_id)[0]
            per_group[grp] += 1
            if grp not in blocked:
                online_now += 1
        return {"total": len(devs), "online_now": online_now, **per_group}

    # ------------------------------------------------------------- Kosten
    def _mb(self, key: str) -> float | None:
        st = self.hass.states.get(self.opt(key) or "")
        val = _float(st)
        if val is None:
            return None
        unit = str(st.attributes.get("unit_of_measurement") or "GB").strip().lower()
        factor = {"gb": 1024, "gib": 1024, "tb": 1048576, "tib": 1048576, "mb": 1, "mib": 1,
                  "kb": 1 / 1024, "kib": 1 / 1024, "b": 1 / 1048576, "bytes": 1 / 1048576}.get(unit, 1024)
        return val * factor

    def _phone_total_mb(self) -> float | None:
        """Summe der Zähler – nur wenn alle eingetragenen Zähler einen Wert haben.

        Fehlt einer kurz (Neustart von HA oder der App), wäre die Summe zu klein und der
        nächste Wert sähe wie neuer Verbrauch aus."""
        vals = [self._mb(k) for k in (CONF_PHONE_RX, CONF_PHONE_TX) if self.opt(k)]
        if not vals or any(v is None for v in vals):
            return None
        return sum(vals)

    @callback
    def _on_usage_event(self, event: Event) -> None:
        total_mb = self._phone_total_mb()
        if total_mb is None:
            return
        u = self.data["usage"]
        last = u.get("last_total")
        u["last_total"] = total_mb
        if last is None:
            self._save()
            return
        if total_mb < last:
            # Zähler kleiner geworden: Handy neu gestartet. Nur zählen, was seitdem dazukam –
            # und nur, wenn der Zähler wirklich von vorn begonnen hat (kleiner Wert).
            delta = total_mb if total_mb < min(50.0, last / 2) else 0.0
            self._save()
        else:
            delta = total_mb - last
        if delta <= 0:
            return
        before = u["mb"]
        u["mb"] = round(before + delta, 3)
        included = float(self.opt(CONF_INCLUDED_MB, DEFAULT_INCLUDED_MB))
        billable = max(0.0, u["mb"] - max(included, before))
        if self.mode != MODE_DAYFLAT and billable > 0:
            u["cost"] = round(u["cost"] + billable * float(self.opt(CONF_PRICE_PER_MB, DEFAULT_PRICE_PER_MB)) / 100, 4)
        self._save()
        self._push()

    def balance(self) -> float:
        u = self.data["usage"]
        start = u.get("start_balance")
        if start is None:
            start = float(self.opt(CONF_START_BALANCE, DEFAULT_START_BALANCE))
        return round(start - u["cost"], 2)

    async def async_reset_usage(self, start_balance: float | None = None) -> None:
        u = self.data["usage"]
        u.update(reset_at=dt_util.utcnow().isoformat(), mb=0.0, cost=0.0, flats=0,
                 start_balance=start_balance)
        self._save()
        self._push()

    def breakeven_mb(self) -> float | None:
        price = float(self.opt(CONF_PRICE_PER_MB, DEFAULT_PRICE_PER_MB))
        if price <= 0:
            return None
        return round(float(self.opt(CONF_DAYFLAT_PRICE, DEFAULT_DAYFLAT_PRICE)) / price * 100, 0)

    # ------------------------------------------------------------- Handy
    def phone(self) -> dict:
        def st(key):
            ent = self.opt(key)
            return self.hass.states.get(ent) if ent else None

        states = [s for s in (st(k) for k in PHONE_KEYS) if s is not None]
        # Lebenszeichen: jede Entität des Handy-Geräts zählt (z. B. WLAN-Signal)
        seen = [s.last_reported for s in states]
        for eid in self._phone_device_entities():
            o = self.hass.states.get(eid)
            if o is not None and o.state not in (STATE_UNAVAILABLE,):
                seen.append(o.last_reported)
        last = max(seen, default=None)
        stale = int(self.opt(CONF_PHONE_STALE_MIN, DEFAULT_PHONE_STALE_MIN))
        reporting = bool(last and dt_util.utcnow() - last < timedelta(minutes=stale))
        charger, data_on = st(CONF_PHONE_CHARGER), st(CONF_PHONE_MOBILE_DATA)
        net, sig, op, bat = st(CONF_PHONE_NETWORK), st(CONF_PHONE_SIGNAL), st(CONF_PHONE_OPERATOR), st(CONF_PHONE_BATTERY)
        return {
            "configured": bool(states),
            "reporting": reporting,
            "last_seen": last.isoformat() if last else None,
            "battery": _float(bat),
            "charging": bool(charger and charger.state.lower() in ("usb", "ac", "on", "charging", "wireless")),
            "charger": charger.state if charger else None,
            "usb": bool(charger and charger.state.lower() == "usb"),
            "mobile_data": None if data_on is None else data_on.state == "on",
            "network": net.state if net else None,
            "signal": _float(sig),
            "operator": op.state if op else None,
            "wifi": self._phone_wifi(),
            "wifi_name": st(CONF_PHONE_WIFI).state if st(CONF_PHONE_WIFI) else None,
            "wake": bool(self.opt(CONF_PHONE_NOTIFY)),
            "woken_at": self.data.get("phone_woken_at"),
        }

    def _phone_device_entities(self) -> list[str]:
        """Alle Entitäten der Geräte, zu denen die Handy-Sensoren gehören."""
        ents = [self.opt(k) for k in PHONE_KEYS if self.opt(k)]
        if not ents:
            return []
        key = tuple(ents)
        cache = getattr(self, "_phone_dev_cache", None)
        if cache and cache[0] == key and (dt_util.utcnow() - cache[1]) < timedelta(minutes=10):
            return cache[2]
        ereg = er.async_get(self.hass)
        devices = {e.device_id for e in (ereg.async_get(x) for x in ents) if e and e.device_id}
        out = sorted({e.entity_id for d in devices for e in er.async_entries_for_device(ereg, d)} - set(ents))
        self._phone_dev_cache = (key, dt_util.utcnow(), out)
        return out

    async def async_wake_phone(self, reason: str = "") -> bool:
        """Companion-App per Push bitten, alle Sensoren sofort zu senden."""
        svc = self.opt(CONF_PHONE_NOTIFY)
        if not svc:
            return False
        domain, _, name = svc.partition(".")
        if not name:
            domain, name = "notify", svc
        try:
            await self.hass.services.async_call(domain, name, {"message": WAKE_MESSAGE}, blocking=True)
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning("Weckruf an %s fehlgeschlagen: %s", svc, err)
            return False
        self.data["phone_woken_at"] = dt_util.utcnow().isoformat()
        _LOGGER.debug("Handy geweckt (%s)", reason)
        self._push()
        return True

    def _wake_due(self) -> bool:
        if not self.opt(CONF_PHONE_NOTIFY):
            return False
        mins = int(self.opt(CONF_PHONE_WAKE_MIN, DEFAULT_PHONE_WAKE_MIN))
        ph_last = self.phone()["last_seen"]
        now = dt_util.utcnow()
        if ph_last and now - dt_util.parse_datetime(ph_last) < timedelta(minutes=mins):
            return False
        woken = self.data.get("phone_woken_at")
        return not (woken and now - dt_util.parse_datetime(woken) < timedelta(minutes=mins))

    # ------------------------------------------------------------- Neueinwahl
    @property
    def reconnect_configured(self) -> bool:
        if self.opt(CONF_RECONNECT_METHOD, METHOD_PPPD_HUP) == METHOD_HA_ACTION:
            return bool(self.opt(CONF_RECONNECT_ENTITY))
        return bool(self.opt(CONF_SSH_HOST) and self.opt(CONF_SSH_PASSWORD))

    @property
    def reconnect_enabled(self) -> bool:
        val = self.data["reconnect"].get("enabled")
        if val is None:
            val = bool(self.opt(CONF_RECONNECT_ENABLED, False))
        return val and self.reconnect_configured

    @property
    def reconnect_time(self) -> dtime:
        raw = self.data["reconnect"].get("time") or self.opt(CONF_RECONNECT_TIME, DEFAULT_RECONNECT_TIME)
        return dtime.fromisoformat(raw)

    async def async_set_reconnect(self, enabled: bool | None = None, at: dtime | None = None) -> None:
        if enabled is not None:
            self.data["reconnect"]["enabled"] = enabled
        if at is not None:
            self.data["reconnect"]["time"] = at.strftime("%H:%M:%S")
        self._schedule_reconnect()
        self._save()
        self._push()

    def _schedule_reconnect(self) -> None:
        if getattr(self, "_rc_unsub", None):
            self._rc_unsub()
            self._rc_unsub = None
        if not self.reconnect_enabled:
            return
        t = self.reconnect_time
        self._rc_unsub = async_track_time_change(self.hass, self._scheduled_reconnect,
                                                 hour=t.hour, minute=t.minute, second=t.second)

    async def _scheduled_reconnect(self, _now=None) -> None:
        if self.mode != MODE_NORMAL:
            _LOGGER.info("Geplante Neueinwahl ausgelassen, Notbetrieb aktiv")
            return
        await self.async_reconnect()

    async def async_reconnect(self) -> str:
        if self.reconnect_running or not self.reconnect_configured:
            return RESULT_ERROR
        self.reconnect_running = True
        self._planned_until = dt_util.utcnow() + timedelta(seconds=RECONNECT_GRACE)
        self._push()
        error = None
        method = self.opt(CONF_RECONNECT_METHOD, METHOD_PPPD_HUP)
        try:
            if method in SSH_METHODS:
                client = SSHClient(self.opt(CONF_SSH_HOST), int(self.opt(CONF_SSH_PORT, DEFAULT_SSH_PORT)),
                                   self.opt(CONF_SSH_USER, DEFAULT_SSH_USER), self.opt(CONF_SSH_PASSWORD))
                result, old_ip, new_ip = await client.reconnect(method, self.opt(CONF_PPP_INTERFACE, DEFAULT_PPP_INTERFACE))
            else:
                result, old_ip, new_ip = await self._reconnect_via_ha()
        except (SSHError, ValueError, HomeAssistantError) as err:
            result, old_ip, new_ip, error = RESULT_ERROR, None, None, str(err)
        finally:
            self.reconnect_running = False
            self._planned_until = dt_util.utcnow() + timedelta(seconds=RECONNECT_GRACE)
        r = self.data["reconnect"]
        if result == RESULT_NO_EFFECT and not error:
            error = "Befehl gesendet, aber die Verbindung wurde nicht getrennt"
        r.update(last=dt_util.utcnow().isoformat(), result=result, old_ip=old_ip, ip=new_ip or old_ip, error=error)
        self.hass.bus.async_fire(EVENT_RECONNECTED, {"result": result, "old_ip": old_ip, "new_ip": new_ip, "error": error})
        if result not in (RESULT_NEW_IP, RESULT_SAME_IP):
            await self.notify(MSG_RECONNECT_FAILED, "Internet: Neueinwahl fehlgeschlagen",
                              f"Ergebnis: {result}" + (f" – {error}" if error else ""))
        self._save()
        self._push()
        return result

    def _ip_now(self) -> str | None:
        st = self._state(CONF_WAN_IP_ENTITY)
        if st is None or st.state in (STATE_UNAVAILABLE, STATE_UNKNOWN, ""):
            return None
        return st.state

    async def _reconnect_via_ha(self) -> tuple[str, str | None, str | None]:
        """Neueinwahl über eine HA-Entität auslösen, z. B. den FRITZ!Box-Button „Neu verbinden“."""
        ent = self.opt(CONF_RECONNECT_ENTITY)
        domain = ent.split(".", 1)[0]
        service = {"button": "press", "script": "turn_on", "input_button": "press"}.get(domain, "turn_on")
        old_ip = self._ip_now()
        prim = self.opt(CONF_PRIMARY_STATUS_ENTITY)
        await self.hass.services.async_call(domain, service, {"entity_id": ent}, blocking=True)
        if not old_ip and not prim:
            return RESULT_TRIGGERED, None, None
        seen_down = False
        loop = asyncio.get_running_loop()
        deadline = loop.time() + RECONNECT_WAIT
        while loop.time() < deadline:
            await asyncio.sleep(RECONNECT_POLL)
            ip = self._ip_now()
            pst = self.hass.states.get(prim) if prim else None
            if ip is None or (pst is not None and pst.state == "off"):
                seen_down = True
                continue
            if old_ip and ip != old_ip:
                return RESULT_NEW_IP, old_ip, ip
            if seen_down:
                return RESULT_SAME_IP, old_ip, ip
        return RESULT_NO_EFFECT, old_ip, None

    # ------------------------------------------------------------- Meldungen
    def notify_targets(self) -> list[dict]:
        """Empfänger, alte Einstellung (nur Dienstliste) wird übernommen."""
        targets = self.opt(CONF_NOTIFY_TARGETS)
        if targets:
            return targets
        return [{"id": f"s{i}", "label": svc, "service": svc, "recipient": "", "sms": False}
                for i, svc in enumerate(self.opt(CONF_NOTIFY, []) or [])]

    def notify_routes(self) -> dict[str, list[str]]:
        routes = self.opt(CONF_NOTIFY_ROUTES)
        ids = [t["id"] for t in self.notify_targets()]
        if routes is None:
            return {m: list(ids) for m in MESSAGES}
        return {m: [i for i in routes.get(m, ids) if i in ids] for m in MESSAGES}

    async def notify(self, key: str, title: str, message: str) -> None:
        targets = {t["id"]: t for t in self.notify_targets()}
        for tid in self.notify_routes().get(key, []):
            t = targets.get(tid)
            if t:
                await self._send(t, title, message)

    async def _send(self, target: dict, title: str, message: str) -> None:
        svc = (target.get("service") or "").strip()
        recipients = [r.strip() for r in str(target.get("recipient") or "").split(",") if r.strip()]
        text = f"{title}: {message}" if target.get("sms") else message
        domain, _, name = svc.partition(".")
        if not name:
            domain, name = "notify", domain
        try:
            if domain == "script":
                await self.hass.services.async_call("script", "turn_on", {
                    "entity_id": svc, "variables": {"title": title, "message": message, "text": text,
                                                    "recipient": recipients}}, blocking=False)
            elif domain == "persistent_notification":
                await self.hass.services.async_call("persistent_notification", "create", {
                    "title": title, "message": message, "notification_id": f"{DOMAIN}_{self.entry.entry_id}"})
            elif self.hass.states.get(svc) and domain == "notify":
                data = {"entity_id": svc, "message": text}
                if not target.get("sms"):
                    data["title"] = title
                await self.hass.services.async_call("notify", "send_message", data, blocking=True)
            elif self.hass.services.has_service(domain, name):
                data: dict[str, Any] = {"message": text}
                if not target.get("sms"):
                    data["title"] = title
                if recipients:
                    data["target"] = recipients
                await self.hass.services.async_call(domain, name, data, blocking=True)
            else:
                _LOGGER.warning("Benachrichtigungsdienst %s gibt es nicht", svc)
        except Exception as err:  # noqa: BLE001 - Meldung darf nie den Ablauf stoppen
            _LOGGER.warning("Meldung über %s fehlgeschlagen: %s", svc, err)

    async def async_test_notify(self, target_id: str | None = None) -> None:
        for t in self.notify_targets():
            if target_id in (None, t["id"]):
                await self._send(t, "HomeLines: Testmeldung", "So sehen Meldungen von HomeLines bei dir aus.")

    # ------------------------------------------------------------- Wächter
    async def _async_watch(self, _now=None) -> None:
        """Backup-Leitung und Notfall-Handy im Normalbetrieb im Blick behalten."""
        w = self.data.setdefault("watch", {"backup_down_since": None, "backup_notified": False,
                                           "phone_notified": False})
        now = dt_util.utcnow()
        backup = next((l for l in self.wan_lines() if l["backup"]), None)
        down = bool(backup and backup["state"] in ("offline", "unavailable") and self.mode == MODE_NORMAL
                    and self.standby == STANDBY_WARM)
        if down:
            if not w["backup_down_since"]:
                w["backup_down_since"] = now.isoformat()
            since = dt_util.parse_datetime(w["backup_down_since"])
            limit = timedelta(minutes=float(self.opt(CONF_BACKUP_DOWN_MIN, DEFAULT_BACKUP_DOWN_MIN)))
            if not w["backup_notified"] and now - since >= limit:
                w["backup_notified"] = True
                await self.notify(MSG_BACKUP_DOWN, "Internet: Backup-Leitung ausgefallen",
                                  f"Das Internet läuft, aber {backup['name']} ist nicht verfügbar. "
                                  "Fällt jetzt die Hauptleitung aus, gibt es keinen Notbetrieb. "
                                  "Tethering und Handy am Notfall-Router prüfen.")
        elif w["backup_down_since"]:
            if w["backup_notified"]:
                await self.notify(MSG_BACKUP_DOWN, "Internet: Backup-Leitung wieder bereit",
                                  f"{backup['name'] if backup else 'Die Backup-Leitung'} ist wieder verfügbar.")
            w.update(backup_down_since=None, backup_notified=False)
        if self._wake_due():
            await self.async_wake_phone("still")
        ph = self.phone()
        if ph["configured"] and not ph["reporting"]:
            if not w["phone_notified"]:
                w["phone_notified"] = True
                await self.notify(MSG_PHONE_SILENT, "Internet: Notfall-Handy meldet sich nicht",
                                  "Das Handy am Notfall-Router hat sich länger nicht bei Home Assistant gemeldet. "
                                  "Ist es eingeschaltet und die Home-Assistant-App aktiv?")
        elif w.get("phone_notified"):
            w["phone_notified"] = False
        self._check_return()
        if self.detection != DETECT_MONITOR:
            await self._async_check_wan()
        self._save()

    @staticmethod
    def _eur(v: float) -> str:
        return f"{float(v):.2f} €".replace(".", ",")

    # ------------------------------------------------------------- Snapshot
    def outage_stats(self) -> dict:
        now = dt_util.utcnow()
        last = self.log.outages[-1] if self.log.outages else None
        return {
            "internet": self.internet, "router": self.router_ok, "latency": self.latency, "loss": self.loss,
            "outages_24h": self.log.count(now, 1), "outages_7d": self.log.count(now, 7),
            "outages_30d": self.log.count(now, 30), "downtime_7d": self.log.downtime(now, 7),
            "availability_7d": self.log.availability(now, 7), "availability_30d": self.log.availability(now, 30),
            "last_outage": last, "recent": self.log.recent(),
            "current_outage": self.log.current,
        }

    def snapshot(self) -> dict:
        m, u, r = self.data["mode"], self.data["usage"], self.data["reconnect"]
        devices = []
        for d in self.inventory.devices:
            grp, src = self.group_of_device(d.id, d.network_id)
            devices.append({**d.as_dict(), "group": grp, "source": src})
        groups = self.data["groups"]["networks"]
        return {
            "entry_id": self.entry.entry_id,
            "title": self.entry.title,
            "mode": m["mode"], "since": m.get("since"), "booked_at": m.get("booked_at"),
            "flat_end": m.get("flat_end"), "restore_at": m.get("restore_at"),
            "planned": self._planned(),
            "wans": self.wan_lines(), "active_wan": self.active_wan(), "backup_wan": self.backup_wan(),
            "router_type": self.opt(CONF_ROUTER_TYPE, ROUTER_NONE), "router_error": self.router_error,
            "persistent": self.adapter.persistent,
            "counts": self.counts(),
            "devices": devices,
            "networks": [{"id": n.id, "name": n.name, "group": groups.get(n.id)} for n in self.inventory.networks]
            + self.missing_networks,
            "wan_missing": self.wan_missing,
            "details": self.details(),
            "default_group": self.opt(CONF_DEFAULT_GROUP, DEFAULT_GROUP),
            "supports_networks": self.adapter.supports_networks,
            "usage": {"reset_at": u["reset_at"], "mb": round(u["mb"], 1), "cost": round(u["cost"], 2),
                      "balance": self.balance(), "flats": u.get("flats", 0),
                      "breakeven_mb": self.breakeven_mb()},
            "tariff": {"provider": self.opt(CONF_PROVIDER, DEFAULT_PROVIDER),
                       "price_per_mb": float(self.opt(CONF_PRICE_PER_MB, DEFAULT_PRICE_PER_MB)),
                       "dayflat_price": float(self.opt(CONF_DAYFLAT_PRICE, DEFAULT_DAYFLAT_PRICE)),
                       "dayflat_hours": float(self.opt(CONF_DAYFLAT_HOURS, DEFAULT_DAYFLAT_HOURS)),
                       "buffer_minutes": float(self.opt(CONF_BUFFER_MIN, DEFAULT_BUFFER_MIN)),
                       "included_mb": float(self.opt(CONF_INCLUDED_MB, DEFAULT_INCLUDED_MB)),
                       "booking_url": self.opt(CONF_BOOKING_URL)},
            "phone": self.phone(),
            "monitor": self.outage_stats(),
            "reconnect": {"configured": self.reconnect_configured,
                          "method": self.opt(CONF_RECONNECT_METHOD, METHOD_PPPD_HUP), "enabled": self.reconnect_enabled,
                          "time": self.reconnect_time.strftime("%H:%M"), "running": self.reconnect_running,
                          "last": r.get("last"), "result": r.get("result"), "ip": r.get("ip"),
                          "error": r.get("error")},
            "emergencies": self.data["history"]["emergencies"][-10:],
            "standby": self.standby, "detection": self.detection,
            "assistant": self.assistant(),
            "pending_since": self._down_since.isoformat() if self._down_since and self.mode == MODE_NORMAL else None,
            "detect_delay": self.detect_delay,
        }
