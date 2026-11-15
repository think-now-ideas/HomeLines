"""HomeLines – Internet Monitor & Mobile Failover."""

from __future__ import annotations

from pathlib import Path

import voluptuous as vol

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import config_validation as cv, entity_registry as er
from homeassistant.util import dt as dt_util

from .const import (
    CARD_URL,
    CONF_BACKUP_EXTRA,
    CONF_SPEED_DOWN,
    CONF_SPEED_EXTRA,
    CONF_SPEED_UP,
    DOMAIN,
    GROUPS,
    LINE_DETAIL_KEYS,
    LINE_HISTORY_KEYS,
    LINE_NAME_KEYS,
    PLATFORMS,
    VERSION,
)
from .hub import FlatError, HomeLinesHub
from .websocket import async_register_websocket

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    path = Path(__file__).parent / "www" / "homelines-card.js"
    await hass.http.async_register_static_paths([StaticPathConfig(CARD_URL, str(path), False)])
    add_extra_js_url(hass, f"{CARD_URL}?v={VERSION}")
    async_register_websocket(hass)
    _register_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hub = HomeLinesHub(hass, entry)
    await hub.async_start()
    hass.data[DOMAIN][entry.entry_id] = hub
    _migrate_entity_ids(hass, entry, hub)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_reload))
    return True


async def _reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        hub: HomeLinesHub = hass.data[DOMAIN].pop(entry.entry_id)
        await hub.async_stop()
    return ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Beim Löschen die UniFi-Regel wieder entfernen."""
    hub = HomeLinesHub(hass, entry)
    remove = getattr(hub.adapter, "async_remove", None)
    if remove:
        try:
            await remove()
        except Exception:  # noqa: BLE001
            pass


def _migrate_entity_ids(hass: HomeAssistant, entry: ConfigEntry, hub: HomeLinesHub) -> None:
    """Einmalig: vorhandene Entitäten auf feste IDs wie sensor.homelines_outages_24h umbenennen."""
    if hub.data.get("ids_fixed"):
        return
    reg = er.async_get(hass)
    prefix = f"{entry.entry_id}_"
    for ent in er.async_entries_for_config_entry(reg, entry.entry_id):
        if not ent.unique_id.startswith(prefix):
            continue
        wanted = f"{ent.domain}.homelines_{ent.unique_id[len(prefix):]}"
        if ent.entity_id != wanted and reg.async_get(wanted) is None:
            reg.async_update_entity(ent.entity_id, new_entity_id=wanted)
    hub.data["ids_fixed"] = True
    hub._save()


def get_hub(hass: HomeAssistant, entry_id: str | None) -> HomeLinesHub:
    hubs: dict = hass.data.get(DOMAIN, {})
    if entry_id:
        if entry_id not in hubs:
            raise ServiceValidationError(translation_domain=DOMAIN, translation_key="unknown_entry")
        return hubs[entry_id]
    if not hubs:
        raise ServiceValidationError(translation_domain=DOMAIN, translation_key="unknown_entry")
    return next(iter(hubs.values()))


def _register_services(hass: HomeAssistant) -> None:
    base = {vol.Optional("entry_id"): cv.string}

    async def activate(call: ServiceCall) -> None:
        hub = get_hub(hass, call.data.get("entry_id"))
        booked = call.data.get("booked_at")
        try:
            await hub.async_activate_flat(dt_util.as_utc(booked) if booked else None)
        except FlatError as err:
            raise HomeAssistantError(translation_domain=DOMAIN, translation_key=err.args[0]) from err

    async def restrict(call: ServiceCall) -> None:
        await get_hub(hass, call.data.get("entry_id")).async_restrict()

    async def set_group(call: ServiceCall) -> None:
        hub = get_hub(hass, call.data.get("entry_id"))
        group = call.data["group"]
        for target in call.data["targets"]:
            await hub.async_set_group(call.data["kind"], target, None if group == "inherit" else group)

    async def reset_usage(call: ServiceCall) -> None:
        await get_hub(hass, call.data.get("entry_id")).async_reset_usage(call.data.get("start_balance"))

    async def reconnect(call: ServiceCall) -> None:
        await get_hub(hass, call.data.get("entry_id")).async_reconnect()

    hass.services.async_register(DOMAIN, "activate_dayflat", activate,
                                 vol.Schema({**base, vol.Optional("booked_at"): cv.datetime}))
    hass.services.async_register(DOMAIN, "restrict", restrict, vol.Schema(base))
    hass.services.async_register(DOMAIN, "set_group", set_group, vol.Schema({
        **base, vol.Required("kind", default="device"): vol.In(["device", "network"]),
        vol.Required("targets"): vol.All(cv.ensure_list, [cv.string]),
        vol.Required("group"): vol.In([*GROUPS, "inherit"])}))
    hass.services.async_register(DOMAIN, "reset_usage", reset_usage, vol.Schema(
        {**base, vol.Optional("start_balance"): vol.Coerce(float)}))
    hass.services.async_register(DOMAIN, "reconnect", reconnect, vol.Schema(base))

    async def test_notify(call: ServiceCall) -> None:
        await get_hub(hass, call.data.get("entry_id")).async_test_notify()

    hass.services.async_register(DOMAIN, "test_notify", test_notify, vol.Schema(base))

    wan = vol.All(cv.string, vol.Upper, vol.In([f"WAN{i}" for i in range(1, 5)]))
    ents = vol.All(cv.ensure_list, [cv.entity_id])

    async def set_details(call: ServiceCall) -> None:
        """Leitungsnamen und Detailansichten in einem Rutsch setzen (statt im Formular)."""
        hub = get_hub(hass, call.data.get("entry_id"))
        opts = dict(hub.entry.options)
        if call.data.get("replace"):
            for key in [*LINE_NAME_KEYS, *LINE_DETAIL_KEYS, *LINE_HISTORY_KEYS,
                        CONF_SPEED_DOWN, CONF_SPEED_UP, CONF_SPEED_EXTRA, CONF_BACKUP_EXTRA]:
                opts.pop(key, None)
        by_wan = lambda keys: {wid: key for key, wid in keys.items()}  # noqa: E731
        names, values, history = by_wan(LINE_NAME_KEYS), by_wan(LINE_DETAIL_KEYS), by_wan(LINE_HISTORY_KEYS)
        for wid, name in (call.data.get("line_names") or {}).items():
            opts[names[wid]] = name
        for wid, d in (call.data.get("lines") or {}).items():
            if "values" in d:
                opts[values[wid]] = d["values"]
            if "history" in d:
                opts[history[wid]] = d["history"]
        for key in ("speed_download", "speed_upload", "speed_extra", "backup_extra"):
            if key in call.data:
                opts[key] = call.data[key]
        hass.config_entries.async_update_entry(hub.entry, options=opts)

    hass.services.async_register(DOMAIN, "set_details", set_details, vol.Schema({
        **base,
        vol.Optional("line_names"): {wan: cv.string},
        vol.Optional("lines"): {wan: vol.Schema({vol.Optional("values"): ents, vol.Optional("history"): ents})},
        vol.Optional("speed_download"): cv.entity_id,
        vol.Optional("speed_upload"): cv.entity_id,
        vol.Optional("speed_extra"): ents,
        vol.Optional("backup_extra"): ents,
        vol.Optional("replace", default=False): cv.boolean,
    }))
