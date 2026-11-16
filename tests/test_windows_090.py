"""Fenster aus Bausteinen (ab 0.9.0): speichern, prüfen, zurücksetzen, über Neustart behalten."""

from __future__ import annotations

from custom_components.homelines.const import DOMAIN
from custom_components.homelines.windows import clean_block, clean_windows

from test_homelines import _setup

DSL = [
    {"t": "values", "title": "Leitung", "ents": ["sensor.modem_dsl_status", "sensor.modem_dsl_rauschabstand"],
     "rules": [{"c": "err", "any": "any", "grp": "all", "when": "below", "v": "3"}], "style": "tiles"},
    {"t": "chart", "title": "Rauschabstand", "ents": ["sensor.modem_dsl_rauschabstand"], "kind": "line",
     "range": "7d", "mode": "together", "colors": {"sensor.modem_dsl_rauschabstand": "blue"},
     "limit": {"on": True, "v": "6", "dir": "below", "c": "err"}, "stats": True},
    {"t": "actions", "title": "Neueinwahl", "ents": ["switch.homelines_taegliche_neueinwahl"]},
    {"t": "log", "title": "Ausfälle", "src": "outages", "n": 4, "style": "timeline"},
    {"t": "text", "text": "Hinweis", "tone": "warn"},
]


def test_clean_keeps_valid_blocks():
    assert clean_windows({"WAN2": DSL}) == {"WAN2": DSL}


def test_clean_drops_unknown_and_bad_values():
    w = clean_windows({
        "WAN2": [
            {"t": "iframe", "src": "https://example.com"},          # unbekannter Baustein
            {"t": "chart", "ents": ["sensor.a", "kein id", "sensor.a"], "kind": "pie", "range": "1y",
             "colors": {"sensor.a": "neon", "sensor.fremd": "blue"}, "limit": "x"},
            {"t": "values", "ents": "sensor.a", "rules": [{"when": "drop table"}, {"when": "above", "v": 5, "c": "err"}]},
            {"t": "log", "src": "geheim", "n": "viele"},
        ],
        "../böse": [{"t": "text", "text": "x"}],                     # unzulässiger Schlüssel
        "speed": "keine Liste",
    })
    assert list(w) == ["WAN2"]
    chart, values, log = w["WAN2"]
    assert chart["ents"] == ["sensor.a"] and chart["kind"] == "line" and chart["range"] == "24h"
    assert chart["colors"] == {} and chart["limit"]["on"] is False
    assert values["ents"] == [] and values["rules"] == [{"c": "err", "any": "any", "grp": "all", "when": "above", "v": "5"}]
    assert log["src"] == "outages" and log["n"] == 5


def test_clean_text_is_limited():
    b = clean_block({"t": "text", "text": "x" * 2000, "tone": "<script>"})
    assert len(b["text"]) == 500 and b["tone"] == "info"


async def test_set_windows_websocket_and_restart(hass, unifi, ping, hass_ws_client):
    entry, hub = await _setup(hass)
    assert hub.snapshot()["windows"] == {}
    ws = await hass_ws_client(hass)

    await ws.send_json({"id": 1, "type": "homelines/set_windows", "key": "WAN2", "blocks": DSL})
    r = await ws.receive_json()
    assert r["success"], r
    assert r["result"] == {"WAN2": DSL}
    assert hub.snapshot()["windows"]["WAN2"][1]["limit"]["v"] == "6"

    # zweites Fenster dazu, erstes bleibt
    await ws.send_json({"id": 2, "type": "homelines/set_windows", "key": "r5",
                        "blocks": [{"t": "values", "title": "Strom", "ents": ["sensor.steckdose_leistung"]}]})
    r = await ws.receive_json()
    assert set(r["result"]) == {"WAN2", "r5"}

    # zurücksetzen: ohne blocks
    await ws.send_json({"id": 3, "type": "homelines/set_windows", "key": "r5"})
    r = await ws.receive_json()
    assert set(r["result"]) == {"WAN2"}

    # über einen Neustart der Integration erhalten
    assert await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    assert hass.data[DOMAIN][entry.entry_id].windows() == {"WAN2": DSL}


async def test_set_windows_needs_admin(hass, unifi, ping, hass_ws_client, hass_read_only_access_token):
    await _setup(hass)
    ws = await hass_ws_client(hass, hass_read_only_access_token)
    await ws.send_json({"id": 1, "type": "homelines/set_windows", "key": "WAN2", "blocks": DSL})
    r = await ws.receive_json()
    assert not r["success"] and r["error"]["code"] == "unauthorized"


# ---------------------------------------------------------------------- 0.9.1: Aufbau der Karte
from custom_components.homelines.windows import clean_layout  # noqa: E402

LAYOUT = {"title": "", "hide_lines": ["WAN1"], "rows": [
    {"id": "t-strom", "kind": "tile", "on": True, "name": "Strom", "icon": "mdi:flash",
     "entities": ["sensor.steckdose_router_leistung"], "combine": "sum",
     "rules": [{"c": "warn", "any": "any", "grp": "all", "when": "unavail", "v": ""}], "second": "bad"},
    {"id": "WAN2", "kind": "builtin", "on": True},
    {"id": "backup", "kind": "builtin", "on": False},
    {"id": "speed", "kind": "builtin", "on": True},
    {"id": "outages", "kind": "builtin", "on": True},
]}


def test_clean_layout():
    assert clean_layout(LAYOUT) == LAYOUT
    bad = clean_layout({"title": "x" * 99, "hide_lines": ["WAN9x", "WAN3"], "rows": [
        {"id": "speed", "kind": "builtin"}, {"id": "speed", "kind": "builtin"},     # doppelt
        {"id": "irgendwas", "kind": "builtin"},                                        # unbekannt
        {"id": "t-a", "kind": "tile", "icon": "javascript:x", "combine": "?", "entities": ["kein id"]}]})
    assert len(bad["title"]) == 40 and bad["hide_lines"] == ["WAN3"]
    assert [r["id"] for r in bad["rows"]] == ["speed", "t-a"]
    assert bad["rows"][1]["icon"] == "mdi:information-outline" and bad["rows"][1]["combine"] == "single"
    assert bad["rows"][1]["entities"] == []


async def test_set_layout_and_line_names(hass, unifi, ping, hass_ws_client):
    entry, hub = await _setup(hass)
    assert hub.snapshot()["layout"] is None
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "homelines/set_layout", "layout": LAYOUT})
    r = await ws.receive_json()
    assert r["success"] and r["result"] == LAYOUT
    await ws.send_json({"id": 2, "type": "homelines/set_layout", "line_names": {"WAN2": "Kupfer", "WAN7": "x"}})
    r = await ws.receive_json()
    assert r["success"]
    await hass.async_block_till_done()
    assert entry.options["line_name_wan2"] == "Kupfer" and "line_name_wan7" not in entry.options
    hub = hass.data[DOMAIN][entry.entry_id]          # nach dem Neuladen
    assert hub.layout() == LAYOUT
    assert {w["id"]: w["name"] for w in hub.snapshot()["wans"]}["WAN2"] == "Kupfer"
