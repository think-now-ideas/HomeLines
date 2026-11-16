"""Websocket-Befehle für die HomeLines-Karte."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.util import dt as dt_util

from .const import DOMAIN, GROUPS, SIGNAL_UPDATE
from .hub import FlatError


def _hub(hass, msg):
    hubs = hass.data.get(DOMAIN, {})
    if msg.get("entry_id"):
        return hubs.get(msg["entry_id"])
    return next(iter(hubs.values()), None)


@callback
def async_register_websocket(hass: HomeAssistant) -> None:
    for handler in (ws_entries, ws_subscribe, ws_activate, ws_restrict, ws_set_group, ws_preview,
                    ws_reset, ws_refresh, ws_dismiss, ws_set_windows):
        websocket_api.async_register_command(hass, handler)


@websocket_api.websocket_command({vol.Required("type"): "homelines/entries"})
@callback
def ws_entries(hass, connection, msg):
    connection.send_result(msg["id"], [
        {"entry_id": h.entry.entry_id, "title": h.entry.title} for h in hass.data.get(DOMAIN, {}).values()])


@websocket_api.websocket_command({vol.Required("type"): "homelines/subscribe",
                                  vol.Optional("entry_id"): str})
@callback
def ws_subscribe(hass, connection, msg):
    hub = _hub(hass, msg)
    if hub is None:
        connection.send_error(msg["id"], "not_found", "HomeLines ist nicht eingerichtet")
        return

    @callback
    def send():
        connection.send_message(websocket_api.event_message(msg["id"], hub.snapshot()))

    connection.subscriptions[msg["id"]] = async_dispatcher_connect(
        hass, SIGNAL_UPDATE.format(hub.entry.entry_id), send)
    connection.send_result(msg["id"])
    send()


def _err(connection, msg, err: FlatError):
    connection.send_error(msg["id"], err.args[0], err.args[0])


@websocket_api.websocket_command({vol.Required("type"): "homelines/preview",
                                  vol.Optional("entry_id"): str, vol.Required("booked_at"): str})
@callback
def ws_preview(hass, connection, msg):
    hub = _hub(hass, msg)
    booked = dt_util.parse_datetime(msg["booked_at"])
    if hub is None or booked is None:
        connection.send_error(msg["id"], "invalid", "Ungültige Eingabe")
        return
    connection.send_result(msg["id"], hub.flat_preview(dt_util.as_utc(booked)))


@websocket_api.websocket_command({vol.Required("type"): "homelines/activate_dayflat",
                                  vol.Optional("entry_id"): str, vol.Optional("booked_at"): str})
@websocket_api.async_response
async def ws_activate(hass, connection, msg):
    hub = _hub(hass, msg)
    booked = dt_util.parse_datetime(msg["booked_at"]) if msg.get("booked_at") else None
    try:
        res = await hub.async_activate_flat(booked)
    except FlatError as err:
        _err(connection, msg, err)
        return
    connection.send_result(msg["id"], res)


@websocket_api.websocket_command({vol.Required("type"): "homelines/restrict",
                                  vol.Optional("entry_id"): str})
@websocket_api.async_response
async def ws_restrict(hass, connection, msg):
    await _hub(hass, msg).async_restrict()
    connection.send_result(msg["id"])


@websocket_api.require_admin
@websocket_api.websocket_command({vol.Required("type"): "homelines/set_group",
                                  vol.Optional("entry_id"): str,
                                  vol.Required("kind"): vol.In(["device", "network"]),
                                  vol.Required("target"): str,
                                  vol.Required("group"): vol.In([*GROUPS, "inherit"])})
@websocket_api.async_response
async def ws_set_group(hass, connection, msg):
    await _hub(hass, msg).async_set_group(msg["kind"], msg["target"],
                                          None if msg["group"] == "inherit" else msg["group"])
    connection.send_result(msg["id"])


@websocket_api.require_admin
@websocket_api.websocket_command({vol.Required("type"): "homelines/reset_usage",
                                  vol.Optional("entry_id"): str,
                                  vol.Optional("start_balance"): vol.Coerce(float)})
@websocket_api.async_response
async def ws_reset(hass, connection, msg):
    await _hub(hass, msg).async_reset_usage(msg.get("start_balance"))
    connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): "homelines/refresh",
                                  vol.Optional("entry_id"): str})
@websocket_api.async_response
async def ws_refresh(hass, connection, msg):
    await _hub(hass, msg)._async_refresh_inventory()
    connection.send_result(msg["id"])


@websocket_api.websocket_command({vol.Required("type"): "homelines/dismiss_return",
                                  vol.Optional("entry_id"): str})
@websocket_api.async_response
async def ws_dismiss(hass, connection, msg):
    await _hub(hass, msg).async_dismiss_return()
    connection.send_result(msg["id"])


@websocket_api.require_admin
@websocket_api.websocket_command({vol.Required("type"): "homelines/set_windows",
                                  vol.Optional("entry_id"): str,
                                  vol.Optional("windows"): dict,
                                  vol.Optional("key"): str,
                                  vol.Optional("blocks"): vol.Any(list, None)})
@websocket_api.async_response
async def ws_set_windows(hass, connection, msg):
    """Fenster speichern (ab 0.9.0). Ohne „blocks“ wird das Fenster auf das eingebaute zurückgesetzt."""
    hub = _hub(hass, msg)
    if hub is None:
        connection.send_error(msg["id"], "not_found", "HomeLines ist nicht eingerichtet")
        return
    await hub.async_set_windows(msg.get("windows"), msg.get("key"), msg.get("blocks"))
    connection.send_result(msg["id"], hub.windows())
