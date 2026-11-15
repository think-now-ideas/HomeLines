"""Einrichtung und Optionen von HomeLines."""

from __future__ import annotations

from typing import Any
from uuid import uuid4
from urllib.parse import urlparse

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector as sel

from .const import (
    CONF_ACTIVE_WAN_ENTITY,
    CONF_API_KEY,
    CONF_BACKUP_WAN,
    CONF_BOOKING_URL,
    CONF_BUFFER_MIN,
    CONF_DAYFLAT_HOURS,
    CONF_DAYFLAT_PRICE,
    CONF_DEFAULT_GROUP,
    CONF_EMERGENCY_INTERVAL,
    CONF_FAILURES,
    CONF_HOST,
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
    DETECT_ACTIVE_WAN,
    DETECTIONS,
    METHOD_HA_ACTION,
    SSH_METHODS,
    STANDBY_WARM,
    STANDBYS,
    CONF_NOTIFY,
    CONF_NOTIFY_ROUTES,
    CONF_NOTIFY_TARGETS,
    DEFAULT_BACKUP_DOWN_MIN,
    MESSAGES,
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
    CONF_PHONE_TX,
    CONF_PING_COUNT,
    CONF_PPP_INTERFACE,
    CONF_PRICE_PER_MB,
    CONF_IMPORTED_FROM,
    CONF_PRIMARY_WAN_LABEL,
    CONF_PRIMARY_WAN_NET,
    CONF_PROVIDER,
    CONF_RECONNECT_ENABLED,
    CONF_RECONNECT_METHOD,
    CONF_RECONNECT_TIME,
    CONF_ROUTER_IP,
    CONF_ROUTER_TYPE,
    CONF_SCRIPT_BLOCK,
    CONF_SCRIPT_UNBLOCK,
    CONF_SITE,
    CONF_SPEEDTEST_SWITCH,
    CONF_SSH_HOST,
    CONF_SSH_PASSWORD,
    CONF_SSH_PORT,
    CONF_SSH_USER,
    CONF_START_BALANCE,
    CONF_SWITCH_ENTITIES,
    CONF_TARGETS,
    CONF_TRACKER_ENTITIES,
    CONF_VERIFY_SSL,
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
    GROUPS,
    METHOD_PPPD_HUP,
    METHODS,
    LEGACY_DOMAIN,
    NAME,
    ROUTER_NONE,
    ROUTER_SCRIPTS,
    ROUTER_SWITCHES,
    ROUTER_TYPES,
    ROUTER_UNIFI,
)
from .reconnect import SSHAuthError, SSHClient, SSHError, validate_interface
from .router import RouterAuthError, RouterError, UnifiAdapter

ENTITY = sel.EntitySelector
TEXT = sel.TextSelector()
PASSWORD = sel.TextSelector(sel.TextSelectorConfig(type=sel.TextSelectorType.PASSWORD))


def _num(lo, hi, step, unit=None):
    cfg = {"min": lo, "max": hi, "step": step, "mode": sel.NumberSelectorMode.BOX}
    if unit:
        cfg["unit_of_measurement"] = unit
    return sel.NumberSelector(sel.NumberSelectorConfig(**cfg))


def _select(options, key, multiple=False, custom=False):
    return sel.SelectSelector(sel.SelectSelectorConfig(options=options, translation_key=key,
                                                       multiple=multiple, custom_value=custom,
                                                       mode=sel.SelectSelectorMode.DROPDOWN))


def _opt(key: str, cur: dict, default: Any = None):
    """vol.Optional mit vorbelegtem Wert, der sich auch leeren lässt."""
    if cur.get(key) not in (None, "", []):
        return vol.Optional(key, description={"suggested_value": cur[key]})
    if default is not None:
        return vol.Optional(key, default=default)
    return vol.Optional(key)


def _host_only(host: str) -> str:
    return urlparse(host if "://" in host else f"//{host}").hostname or host


# ---------------------------------------------------------------- Schemata
def with_wan_label(data: dict, wans: list[dict] | None) -> dict:
    """Zur ID der Hauptleitung auch Name und WAN-Gruppe speichern (für den Abgleich, wenn UniFi neue IDs vergibt)."""
    w = next((w for w in wans or [] if w["id"] == data.get(CONF_PRIMARY_WAN_NET)), None)
    if w:
        data[CONF_PRIMARY_WAN_LABEL] = {"name": w["name"], "group": w.get("group")}
    return data


def _wan_default(cur: dict, wans: list[dict]) -> str:
    """Gespeicherte ID, sonst dieselbe Leitung über Gruppe oder Namen, sonst die erste."""
    ids = [w["id"] for w in wans]
    if cur.get(CONF_PRIMARY_WAN_NET) in ids:
        return cur[CONF_PRIMARY_WAN_NET]
    label = cur.get(CONF_PRIMARY_WAN_LABEL) or {}
    for key, val in (("group", label.get("group")), ("name", label.get("name"))):
        hit = next((w["id"] for w in wans if val and w.get(key) == val), None)
        if hit:
            return hit
    return ids[0]


def lines_schema(cur: dict, wans: list[dict] | None) -> vol.Schema:
    fields: dict = {
        vol.Required(CONF_STANDBY, default=cur.get(CONF_STANDBY, STANDBY_WARM)): _select(STANDBYS, "standby"),
        vol.Required(CONF_DETECTION, default=cur.get(CONF_DETECTION, DETECT_ACTIVE_WAN)):
            _select(DETECTIONS, "detection"),
        _opt(CONF_ACTIVE_WAN_ENTITY, cur): ENTITY(sel.EntitySelectorConfig(domain="sensor")),
        _opt(CONF_PRIMARY_STATUS_ENTITY, cur): ENTITY(sel.EntitySelectorConfig(domain="binary_sensor")),
        _opt(CONF_CUSTOM_DOWN_ENTITY, cur): ENTITY(sel.EntitySelectorConfig(domain=["binary_sensor", "input_boolean"])),
        _opt(CONF_DETECT_DELAY, cur): _num(0, 3600, 10, "s"),
        vol.Required(CONF_BACKUP_WAN, default=cur.get(CONF_BACKUP_WAN, "WAN3")): TEXT,
        _opt(CONF_WAN_STATUS_ENTITIES, cur): ENTITY(sel.EntitySelectorConfig(domain="binary_sensor", multiple=True)),
        _opt(CONF_SPEEDTEST_SWITCH, cur): ENTITY(sel.EntitySelectorConfig(domain="switch")),
        vol.Required(CONF_DEFAULT_GROUP, default=cur.get(CONF_DEFAULT_GROUP, DEFAULT_GROUP)):
            _select(GROUPS, "group"),
    }
    if wans:
        opts = [sel.SelectOptionDict(value=w["id"], label=f"{w['name']} ({w.get('group') or '?'})") for w in wans]
        fields[vol.Required(CONF_PRIMARY_WAN_NET, default=_wan_default(cur, wans))] = \
            sel.SelectSelector(sel.SelectSelectorConfig(options=opts))
    return vol.Schema(fields)


def monitor_schema(cur: dict) -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_TARGETS, default=cur.get(CONF_TARGETS, DEFAULT_TARGETS)): TEXT,
        _opt(CONF_ROUTER_IP, cur): TEXT,  # leer = bei UniFi die Router-Adresse
        vol.Required(CONF_INTERVAL, default=cur.get(CONF_INTERVAL, DEFAULT_INTERVAL)): _num(10, 600, 5, "s"),
        vol.Required(CONF_EMERGENCY_INTERVAL, default=cur.get(CONF_EMERGENCY_INTERVAL, DEFAULT_EMERGENCY_INTERVAL)):
            _num(10, 1800, 10, "s"),
        vol.Required(CONF_PING_COUNT, default=cur.get(CONF_PING_COUNT, DEFAULT_PING_COUNT)): _num(1, 10, 1),
        vol.Required(CONF_FAILURES, default=cur.get(CONF_FAILURES, DEFAULT_FAILURES)): _num(1, 10, 1),
    })


def tariff_schema(cur: dict) -> vol.Schema:
    return vol.Schema({
        vol.Optional(CONF_PROVIDER, default=cur.get(CONF_PROVIDER, DEFAULT_PROVIDER)): TEXT,
        vol.Required(CONF_PRICE_PER_MB, default=cur.get(CONF_PRICE_PER_MB, DEFAULT_PRICE_PER_MB)): _num(0, 100, 0.1, "ct/MB"),
        vol.Required(CONF_INCLUDED_MB, default=cur.get(CONF_INCLUDED_MB, DEFAULT_INCLUDED_MB)): _num(0, 1000000, 1, "MB"),
        vol.Required(CONF_DAYFLAT_PRICE, default=cur.get(CONF_DAYFLAT_PRICE, DEFAULT_DAYFLAT_PRICE)): _num(0, 100, 0.01, "€"),
        vol.Required(CONF_DAYFLAT_HOURS, default=cur.get(CONF_DAYFLAT_HOURS, DEFAULT_DAYFLAT_HOURS)): _num(1, 744, 1, "h"),
        vol.Required(CONF_BUFFER_MIN, default=cur.get(CONF_BUFFER_MIN, DEFAULT_BUFFER_MIN)): _num(0, 240, 5, "min"),
        vol.Required(CONF_START_BALANCE, default=cur.get(CONF_START_BALANCE, DEFAULT_START_BALANCE)): _num(0, 1000, 0.01, "€"),
        _opt(CONF_BOOKING_URL, cur): TEXT,
    })


def phone_schema(cur: dict, hass: HomeAssistant | None = None) -> vol.Schema:
    s = lambda d: ENTITY(sel.EntitySelectorConfig(domain=d))  # noqa: E731
    apps = sorted(f"notify.{x}" for x in (hass.services.async_services_for_domain("notify") if hass else {})
                  if x.startswith("mobile_app_"))
    cur_n = cur.get(CONF_PHONE_NOTIFY)
    if cur_n and cur_n not in apps:
        apps.append(cur_n)
    return vol.Schema({
        _opt(CONF_PHONE_NOTIFY, cur): sel.SelectSelector(sel.SelectSelectorConfig(
            options=apps, custom_value=True, mode=sel.SelectSelectorMode.DROPDOWN)),
        vol.Required(CONF_PHONE_WAKE_MIN, default=cur.get(CONF_PHONE_WAKE_MIN, DEFAULT_PHONE_WAKE_MIN)):
            _num(5, 120, 5, "min"),
        _opt(CONF_PHONE_RX, cur): s("sensor"), _opt(CONF_PHONE_TX, cur): s("sensor"),
        _opt(CONF_PHONE_MOBILE_DATA, cur): s(["binary_sensor", "sensor"]),
        _opt(CONF_PHONE_NETWORK, cur): s("sensor"), _opt(CONF_PHONE_SIGNAL, cur): s("sensor"),
        _opt(CONF_PHONE_OPERATOR, cur): s("sensor"), _opt(CONF_PHONE_BATTERY, cur): s("sensor"),
        _opt(CONF_PHONE_CHARGER, cur): s(["sensor", "binary_sensor"]),
        _opt(CONF_PHONE_WIFI, cur): s("sensor"),
        vol.Required(CONF_PHONE_STALE_MIN, default=cur.get(CONF_PHONE_STALE_MIN, DEFAULT_PHONE_STALE_MIN)):
            _num(5, 1440, 5, "min"),
    })


def notify_options(hass: HomeAssistant) -> list[str]:
    svcs = [f"notify.{s}" for s in hass.services.async_services_for_domain("notify")
            if s not in ("send_message", "persistent_notification")]
    ents = [e for e in hass.states.async_entity_ids("notify")]
    scripts = list(hass.states.async_entity_ids("script"))
    return sorted(set(svcs + ents)) + ["persistent_notification.create"] + sorted(scripts)


def targets_of(cur: dict) -> list[dict]:
    if cur.get(CONF_NOTIFY_TARGETS):
        return [dict(t) for t in cur[CONF_NOTIFY_TARGETS]]
    return [{"id": f"s{i}", "label": svc, "service": svc, "recipient": "", "sms": False}
            for i, svc in enumerate(cur.get(CONF_NOTIFY, []) or [])]


def routes_of(cur: dict, targets: list[dict]) -> dict:
    ids = [t["id"] for t in targets]
    routes = cur.get(CONF_NOTIFY_ROUTES)
    if routes is None:
        return {m: list(ids) for m in MESSAGES}
    return {m: [i for i in routes.get(m, ids) if i in ids] for m in MESSAGES}


def target_schema(hass: HomeAssistant, t: dict, edit: bool = False) -> vol.Schema:
    opts = sorted(set(notify_options(hass) + ([t["service"]] if t.get("service") else [])))
    fields = {
        vol.Required("label", default=t.get("label", "")): TEXT,
        vol.Required("service", default=t.get("service") or (opts[0] if opts else "")): sel.SelectSelector(
            sel.SelectSelectorConfig(options=opts, custom_value=True, mode=sel.SelectSelectorMode.DROPDOWN)),
        vol.Optional("recipient", default=t.get("recipient", "")): TEXT,
        vol.Required("sms", default=t.get("sms", False)): sel.BooleanSelector(),
    }
    if edit:
        fields[vol.Required("remove", default=False)] = sel.BooleanSelector()
    return vol.Schema(fields)


def messages_schema(cur: dict, targets: list[dict]) -> vol.Schema:
    routes = routes_of(cur, targets)
    opts = [sel.SelectOptionDict(value=t["id"], label=t["label"]) for t in targets]
    fields: dict = {}
    for m in MESSAGES:
        fields[vol.Optional(m, default=routes[m])] = sel.SelectSelector(
            sel.SelectSelectorConfig(options=opts, multiple=True, mode=sel.SelectSelectorMode.LIST))
    fields[vol.Required(CONF_BACKUP_DOWN_MIN, default=cur.get(CONF_BACKUP_DOWN_MIN, DEFAULT_BACKUP_DOWN_MIN))] = \
        _num(1, 1440, 1, "min")
    return vol.Schema(fields)


def reconnect_schema(cur: dict, host_default: str | None) -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_RECONNECT_ENABLED, default=cur.get(CONF_RECONNECT_ENABLED, False)): sel.BooleanSelector(),
        vol.Required(CONF_RECONNECT_METHOD, default=cur.get(CONF_RECONNECT_METHOD, METHOD_PPPD_HUP)):
            _select(METHODS, "method"),
        vol.Required(CONF_RECONNECT_TIME, default=cur.get(CONF_RECONNECT_TIME, DEFAULT_RECONNECT_TIME)):
            sel.TimeSelector(),
        _opt(CONF_RECONNECT_ENTITY, cur): ENTITY(sel.EntitySelectorConfig(domain=["button", "script", "switch", "input_button"])),
        _opt(CONF_WAN_IP_ENTITY, cur): ENTITY(sel.EntitySelectorConfig(domain="sensor")),
        vol.Optional(CONF_SSH_HOST, default=cur.get(CONF_SSH_HOST) or host_default or ""): TEXT,
        vol.Required(CONF_SSH_PORT, default=cur.get(CONF_SSH_PORT, DEFAULT_SSH_PORT)): _num(1, 65535, 1),
        vol.Required(CONF_SSH_USER, default=cur.get(CONF_SSH_USER, DEFAULT_SSH_USER)): TEXT,
        _opt(CONF_SSH_PASSWORD, cur): PASSWORD,
        vol.Required(CONF_PPP_INTERFACE, default=cur.get(CONF_PPP_INTERFACE, DEFAULT_PPP_INTERFACE)): TEXT,
    })


def unifi_schema(cur: dict) -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_HOST, default=cur.get(CONF_HOST, "")): TEXT,
        vol.Required(CONF_API_KEY, default=cur.get(CONF_API_KEY, "")): PASSWORD,
        vol.Required(CONF_SITE, default=cur.get(CONF_SITE, "default")): TEXT,
        vol.Required(CONF_VERIFY_SSL, default=cur.get(CONF_VERIFY_SSL, False)): sel.BooleanSelector(),
    })


def switches_schema(cur: dict) -> vol.Schema:
    return vol.Schema({vol.Required(CONF_SWITCH_ENTITIES, default=cur.get(CONF_SWITCH_ENTITIES, [])):
                       ENTITY(sel.EntitySelectorConfig(domain="switch", multiple=True))})


def scripts_schema(cur: dict) -> vol.Schema:
    return vol.Schema({
        _opt(CONF_SCRIPT_BLOCK, cur): ENTITY(sel.EntitySelectorConfig(domain="script")),
        _opt(CONF_SCRIPT_UNBLOCK, cur): ENTITY(sel.EntitySelectorConfig(domain="script")),
        vol.Required(CONF_TRACKER_ENTITIES, default=cur.get(CONF_TRACKER_ENTITIES, [])):
            ENTITY(sel.EntitySelectorConfig(domain="device_tracker", multiple=True)),
    })


# ---------------------------------------------------------------- Prüfungen
async def validate_unifi(hass, data: dict) -> tuple[dict, list[dict]]:
    errors: dict = {}
    wans: list[dict] = []
    try:
        inv = await UnifiAdapter(hass, data).async_test()
        wans = [{"id": w.id, "name": w.name, "group": w.wan_group} for w in inv.wans]
        if not wans:
            errors["base"] = "no_wan"
    except RouterAuthError:
        errors["base"] = "invalid_auth"
    except RouterError:
        errors["base"] = "cannot_connect"
    return errors, wans


async def validate_ssh(data: dict) -> dict:
    if data.get(CONF_RECONNECT_METHOD) == METHOD_HA_ACTION:
        if data.get(CONF_RECONNECT_ENABLED) and not data.get(CONF_RECONNECT_ENTITY):
            return {CONF_RECONNECT_ENTITY: "entity_missing"}
        return {}
    if not data.get(CONF_RECONNECT_ENABLED) and not data.get(CONF_SSH_PASSWORD):
        return {}
    if not data.get(CONF_SSH_HOST) or not data.get(CONF_SSH_PASSWORD):
        return {"base": "ssh_missing"}
    try:
        validate_interface(data[CONF_PPP_INTERFACE])
    except ValueError:
        return {CONF_PPP_INTERFACE: "invalid_interface"}
    client = SSHClient(data[CONF_SSH_HOST], int(data[CONF_SSH_PORT]), data[CONF_SSH_USER], data[CONF_SSH_PASSWORD])
    try:
        found = await client.interfaces()
    except SSHAuthError:
        return {"base": "ssh_auth"}
    except SSHError:
        return {"base": "ssh_connect"}
    if found and data[CONF_PPP_INTERFACE] not in found:
        return {CONF_PPP_INTERFACE: "interface_not_found"}
    return {}


def _merge(base: dict, schema: vol.Schema, user: dict) -> dict:
    out = dict(base)
    for key in schema.schema:
        k = str(key)
        if k in user:
            out[k] = user[k]
        else:
            out.pop(k, None)
    for k in (CONF_INTERVAL, CONF_EMERGENCY_INTERVAL, CONF_PING_COUNT, CONF_FAILURES, CONF_SSH_PORT,
              CONF_PHONE_STALE_MIN, CONF_PHONE_WAKE_MIN, CONF_DETECT_DELAY):
        if k in out:
            out[k] = int(out[k])
    return out


# ---------------------------------------------------------------- Einrichtung
class HomeLinesConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._wans: list[dict] = []
        self._legacy_asked = False

    @staticmethod
    @callback
    def async_get_options_flow(entry: ConfigEntry) -> OptionsFlow:
        return HomeLinesOptionsFlow()

    def _legacy_entries(self) -> list[ConfigEntry]:
        """LineGuard-Einrichtungen, die noch nicht übernommen wurden."""
        done = {e.data.get(CONF_IMPORTED_FROM) for e in self._async_current_entries(include_ignore=False)}
        return [e for e in self.hass.config_entries.async_entries(LEGACY_DOMAIN) if e.entry_id not in done]

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        if user_input is None and not self._legacy_asked and self._legacy_entries():
            return await self.async_step_legacy()
        if user_input is not None:
            self._data.update(user_input)
            return await getattr(self, f"async_step_{user_input[CONF_ROUTER_TYPE]}")()
        return self.async_show_form(step_id="user", data_schema=vol.Schema({
            vol.Required("name", default=NAME): TEXT,
            vol.Required(CONF_ROUTER_TYPE, default=ROUTER_UNIFI): _select(ROUTER_TYPES, "router_type"),
        }))

    async def async_step_legacy(self, user_input=None) -> ConfigFlowResult:
        """Vorgänger LineGuard gefunden: übernehmen oder neu einrichten."""
        self._legacy_asked = True
        return self.async_show_menu(step_id="legacy", menu_options=["import_legacy", "user"])

    async def async_step_import_legacy(self, user_input=None) -> ConfigFlowResult:
        """Einstellungen von LineGuard übernehmen; Gruppen, Zähler und Historie holt der Hub beim Start."""
        old = self._legacy_entries()[0]
        if old.unique_id:
            await self.async_set_unique_id(old.unique_id)
            self._abort_if_unique_id_configured()
        title = NAME if old.title in ("", "LineGuard") else old.title
        data = {**old.data, CONF_IMPORTED_FROM: old.entry_id}
        return self.async_create_entry(title=title, data=data, options=dict(old.options))

    async def async_step_unifi(self, user_input=None) -> ConfigFlowResult:
        errors: dict = {}
        if user_input is not None:
            errors, self._wans = await validate_unifi(self.hass, user_input)
            if not errors:
                await self.async_set_unique_id(f"unifi_{_host_only(user_input[CONF_HOST])}")
                self._abort_if_unique_id_configured()
                self._data.update(user_input)
                return await self.async_step_lines()
        return self.async_show_form(step_id="unifi", data_schema=unifi_schema(user_input or {}), errors=errors)

    async def async_step_switches(self, user_input=None) -> ConfigFlowResult:
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_lines()
        return self.async_show_form(step_id="switches", data_schema=switches_schema({}))

    async def async_step_scripts(self, user_input=None) -> ConfigFlowResult:
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_lines()
        return self.async_show_form(step_id="scripts", data_schema=scripts_schema({}))

    async def async_step_none(self, user_input=None) -> ConfigFlowResult:
        return await self.async_step_lines()

    async def async_step_lines(self, user_input=None) -> ConfigFlowResult:
        schema = lines_schema({}, self._wans)
        if user_input is not None:
            self._data = with_wan_label(_merge(self._data, schema, user_input), self._wans)
            return await self.async_step_reconnect()
        return self.async_show_form(step_id="lines", data_schema=schema)

    async def async_step_reconnect(self, user_input=None) -> ConfigFlowResult:
        host = _host_only(self._data[CONF_HOST]) if self._data.get(CONF_HOST) else None
        errors: dict = {}
        if user_input is not None:
            errors = await validate_ssh(user_input)
            if not errors:
                self._data.update(user_input)
                title = self._data.pop("name", NAME)
                return self.async_create_entry(title=title, data=self._data, options={})
        return self.async_show_form(step_id="reconnect", data_schema=reconnect_schema(user_input or {}, host),
                                    errors=errors)


# ---------------------------------------------------------------- Optionen
class HomeLinesOptionsFlow(OptionsFlow):
    def __init__(self) -> None:
        self._wans: list[dict] | None = None
        self._edit_id: str | None = None

    @property
    def _cur(self) -> dict:
        return {**self.config_entry.data, **self.config_entry.options}

    async def async_step_init(self, user_input=None) -> ConfigFlowResult:
        menu = ["lines", "tariff", "phone", "notify", "monitor", "reconnect"]
        if self._cur.get(CONF_ROUTER_TYPE) != ROUTER_NONE:
            menu.append("router")
        return self.async_show_menu(step_id="init", menu_options=menu)

    def _save(self, schema: vol.Schema, user_input: dict) -> ConfigFlowResult:
        data = _merge(dict(self.config_entry.options), schema, user_input)
        return self.async_create_entry(data=with_wan_label(data, self._wans))

    async def async_step_lines(self, user_input=None) -> ConfigFlowResult:
        if self._wans is None and self._cur.get(CONF_ROUTER_TYPE) == ROUTER_UNIFI:
            _, self._wans = await validate_unifi(self.hass, self._cur)
        schema = lines_schema(self._cur, self._wans)
        if user_input is not None:
            return self._save(schema, user_input)
        return self.async_show_form(step_id="lines", data_schema=schema)

    async def async_step_monitor(self, user_input=None) -> ConfigFlowResult:
        schema = monitor_schema(self._cur)
        if user_input is not None:
            return self._save(schema, user_input)
        return self.async_show_form(step_id="monitor", data_schema=schema)

    async def async_step_tariff(self, user_input=None) -> ConfigFlowResult:
        schema = tariff_schema(self._cur)
        if user_input is not None:
            return self._save(schema, user_input)
        return self.async_show_form(step_id="tariff", data_schema=schema)

    async def async_step_phone(self, user_input=None) -> ConfigFlowResult:
        schema = phone_schema(self._cur, self.hass)
        if user_input is not None:
            return self._save(schema, user_input)
        return self.async_show_form(step_id="phone", data_schema=schema)

    def _save_notify(self, targets: list[dict], routes: dict, extra: dict | None = None) -> ConfigFlowResult:
        opts = dict(self.config_entry.options)
        opts.pop(CONF_NOTIFY, None)
        opts[CONF_NOTIFY_TARGETS] = targets
        opts[CONF_NOTIFY_ROUTES] = routes
        opts.update(extra or {})
        return self.async_create_entry(data=opts)

    async def async_step_notify(self, user_input=None) -> ConfigFlowResult:
        menu = ["notify_add"]
        if targets_of(self._cur):
            menu += ["notify_pick", "notify_messages"]
        return self.async_show_menu(step_id="notify", menu_options=menu,
                                    description_placeholders={"targets": ", ".join(
                                        t["label"] for t in targets_of(self._cur)) or "–"})

    async def async_step_notify_add(self, user_input=None) -> ConfigFlowResult:
        if user_input is not None:
            targets = targets_of(self._cur)
            routes = routes_of(self._cur, targets)
            new = {"id": uuid4().hex[:8], **{k: user_input.get(k, "") for k in ("label", "service", "recipient")},
                   "sms": bool(user_input.get("sms"))}
            targets.append(new)
            for m in MESSAGES:
                routes[m].append(new["id"])
            return self._save_notify(targets, routes)
        return self.async_show_form(step_id="notify_add", data_schema=target_schema(self.hass, {}))

    async def async_step_notify_pick(self, user_input=None) -> ConfigFlowResult:
        targets = targets_of(self._cur)
        if user_input is not None:
            self._edit_id = user_input["target"]
            return await self.async_step_notify_edit()
        return self.async_show_form(step_id="notify_pick", data_schema=vol.Schema({
            vol.Required("target"): sel.SelectSelector(sel.SelectSelectorConfig(
                options=[sel.SelectOptionDict(value=t["id"], label=t["label"]) for t in targets]))}))

    async def async_step_notify_edit(self, user_input=None) -> ConfigFlowResult:
        targets = targets_of(self._cur)
        t = next(x for x in targets if x["id"] == self._edit_id)
        if user_input is not None:
            routes = routes_of(self._cur, targets)
            if user_input.get("remove"):
                targets = [x for x in targets if x["id"] != t["id"]]
                routes = {m: [i for i in ids if i != t["id"]] for m, ids in routes.items()}
            else:
                t.update({k: user_input.get(k, "") for k in ("label", "service", "recipient")},
                         sms=bool(user_input.get("sms")))
            return self._save_notify(targets, routes)
        return self.async_show_form(step_id="notify_edit", data_schema=target_schema(self.hass, t, edit=True))

    async def async_step_notify_messages(self, user_input=None) -> ConfigFlowResult:
        targets = targets_of(self._cur)
        if user_input is not None:
            routes = {m: list(user_input.get(m, [])) for m in MESSAGES}
            return self._save_notify(targets, routes,
                                     {CONF_BACKUP_DOWN_MIN: int(user_input[CONF_BACKUP_DOWN_MIN])})
        return self.async_show_form(step_id="notify_messages", data_schema=messages_schema(self._cur, targets))

    async def async_step_reconnect(self, user_input=None) -> ConfigFlowResult:
        cur = self._cur
        host = _host_only(cur[CONF_HOST]) if cur.get(CONF_HOST) else None
        schema = reconnect_schema(cur, host)
        errors: dict = {}
        if user_input is not None:
            merged = {**cur, **user_input}
            errors = await validate_ssh(merged)
            if not errors:
                return self._save(schema, user_input)
        return self.async_show_form(step_id="reconnect", data_schema=schema, errors=errors)

    async def async_step_router(self, user_input=None) -> ConfigFlowResult:
        rtype = self._cur.get(CONF_ROUTER_TYPE)
        cur = self._cur
        schema = {ROUTER_UNIFI: unifi_schema, ROUTER_SWITCHES: switches_schema,
                  ROUTER_SCRIPTS: scripts_schema}[rtype](cur)
        errors: dict = {}
        if user_input is not None:
            if rtype == ROUTER_UNIFI:
                errors, self._wans = await validate_unifi(self.hass, {**cur, **user_input})
            if not errors:
                return self._save(schema, user_input)
        return self.async_show_form(step_id="router", data_schema=schema, errors=errors)
