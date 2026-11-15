"""Ende-zu-Ende-Tests für HomeLines."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_time_changed,
    async_mock_service,
)

from custom_components.homelines.const import DOMAIN

BASE = {
    "router_type": "unifi", "host": "192.168.1.1", "api_key": "secret", "site": "default", "verify_ssl": False,
    "active_wan_entity": "sensor.unifi_active_wan_id", "backup_wan": "WAN3",
    "wan_status_entities": ["binary_sensor.unifi_wan2_internet", "binary_sensor.unifi_wan3_internet"],
    "speedtest_switch": "switch.unifi_wan_auto_speedtest", "primary_wan_network": "wan2",
    "reconnect_enabled": False,
}
OPTIONS = {
    "notify_services": ["notify.mobile_app_mein_handy"],
    "phone_rx": "sensor.notfall_handy_mobile_rx_gb", "phone_tx": "sensor.notfall_handy_mobile_tx_gb",
    "phone_charger": "sensor.notfall_handy_charger_type", "phone_mobile_data": "binary_sensor.notfall_handy_mobile_data",
    "phone_signal": "sensor.notfall_handy_signal", "phone_battery": "sensor.notfall_handy_battery",
}


async def _setup(hass: HomeAssistant, options=None):
    hass.states.async_set("sensor.unifi_active_wan_id", "WAN2")
    hass.states.async_set("binary_sensor.unifi_wan2_internet", "on", {"friendly_name": "UniFi WAN2 Internet"})
    hass.states.async_set("binary_sensor.unifi_wan3_internet", "off", {"friendly_name": "UniFi WAN3 Internet"})
    hass.states.async_set("switch.unifi_wan_auto_speedtest", "on")
    hass.states.async_set("sensor.notfall_handy_mobile_rx_gb", "0.032")
    hass.states.async_set("sensor.notfall_handy_mobile_tx_gb", "0.007")
    hass.states.async_set("sensor.notfall_handy_charger_type", "usb")
    hass.states.async_set("binary_sensor.notfall_handy_mobile_data", "on")
    hass.states.async_set("sensor.notfall_handy_signal", "-101")
    hass.states.async_set("sensor.notfall_handy_battery", "93")
    entry = MockConfigEntry(domain=DOMAIN, title="HomeLines", data=BASE,
                            options=OPTIONS if options is None else options)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry, hass.data[DOMAIN][entry.entry_id]


async def test_config_flow(hass, unifi, ping):
    r = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    r = await hass.config_entries.flow.async_configure(r["flow_id"], {"name": "HomeLines", "router_type": "unifi"})
    assert r["step_id"] == "unifi"
    bad = await hass.config_entries.flow.async_configure(
        r["flow_id"], {"host": "192.168.1.1", "api_key": "wrong", "site": "default", "verify_ssl": False})
    assert bad["errors"] == {"base": "invalid_auth"}
    r = await hass.config_entries.flow.async_configure(
        r["flow_id"], {"host": "192.168.1.1", "api_key": "secret", "site": "default", "verify_ssl": False})
    assert r["step_id"] == "lines"
    r = await hass.config_entries.flow.async_configure(r["flow_id"], {
        "active_wan_entity": "sensor.unifi_active_wan_id", "backup_wan": "WAN3", "primary_wan_network": "wan2"})
    assert r["step_id"] == "reconnect"
    r = await hass.config_entries.flow.async_configure(r["flow_id"], {
        "reconnect_enabled": False, "ssh_host": "192.168.1.1", "ssh_port": 22, "ssh_user": "root",
        "ppp_interface": "ppp1", "reconnect_method": "pppd_hup", "reconnect_time": "04:00:00"})
    assert r["type"] is FlowResultType.CREATE_ENTRY
    assert r["data"]["primary_wan_network"] == "wan2"
    await hass.async_block_till_done()


async def test_options_flow(hass, unifi, ping):
    entry, _ = await _setup(hass)
    r = await hass.config_entries.options.async_init(entry.entry_id)
    assert r["type"] is FlowResultType.MENU
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "tariff"})
    r = await hass.config_entries.options.async_configure(r["flow_id"], {
        "provider": "Mobilfunk-Prepaid", "price_per_mb": 3, "included_mb": 0, "dayflat_price": 7.99,
        "dayflat_hours": 24, "buffer_minutes": 30, "start_balance": 20})
    assert r["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert hass.data[DOMAIN][entry.entry_id].balance() == 20.0
    assert entry.options["notify_services"] == ["notify.mobile_app_mein_handy"]


async def test_full_failover_cycle(hass, unifi, ping):
    notes = async_mock_service(hass, "notify", "mobile_app_mein_handy")
    entry, hub = await _setup(hass)
    sw_off = async_mock_service(hass, "switch", "turn_off")
    sw_on = async_mock_service(hass, "switch", "turn_on")

    # Standard: neue Geräte "Mit Tagesflat" -> HA und Handy auf Immer setzen
    await hub.async_set_group("device", "aa:00:00:00:00:01", "always")
    await hub.async_set_group("device", "aa:00:00:00:00:02", "always")
    await hub.async_set_group("network", "guest", "never")
    enabled, targets = unifi.route_targets()
    assert enabled
    assert targets == ["aa:00:00:00:00:03", "aa:00:00:00:00:05", "net:guest"]
    assert all(r["kill_switch_enabled"] and r["network_id"] == "wan2" for r in unifi.routes)
    assert len(unifi.routes) == 1  # keine doppelte Regel
    assert hub.counts()["total"] == 5  # "Alt" ist zu lange nicht gesehen

    # Ausfall der Hauptleitung
    hass.states.async_set("binary_sensor.unifi_wan3_internet", "on")
    hass.states.async_set("sensor.unifi_active_wan_id", "WAN3")
    await hass.async_block_till_done()
    assert hub.mode == "emergency"
    assert hass.states.get("sensor.homelines_status").state == "emergency"
    assert len(notes) == 1 and "Notbetrieb" in notes[0].data["title"]
    assert sw_off and sw_off[0].data["entity_id"] == "switch.unifi_wan_auto_speedtest"
    assert hub.counts()["online_now"] == 2

    # Verbrauch: 50 MB über Mobilfunk = 1,50 €
    hass.states.async_set("sensor.notfall_handy_mobile_rx_gb", str(0.032 + 50 / 1024))
    await hass.async_block_till_done()
    assert round(hub.data["usage"]["cost"], 2) == 1.50

    # Tagesflat vor einer Stunde gebucht
    booked = dt_util.utcnow() - timedelta(hours=1)
    res = await hub.async_activate_flat(booked)
    assert hub.mode == "dayflat"
    restore = dt_util.parse_datetime(res["restore_at"])
    assert abs((restore - (booked + timedelta(hours=23, minutes=30))).total_seconds()) < 1
    enabled, targets = unifi.route_targets()
    assert targets == ["net:guest"]
    assert round(hub.data["usage"]["cost"], 2) == round(1.50 + 7.99, 2)
    # Während der Tagesflat kostet Verbrauch nichts extra
    hass.states.async_set("sensor.notfall_handy_mobile_rx_gb", str(0.032 + 500 / 1024))
    await hass.async_block_till_done()
    assert round(hub.data["usage"]["cost"], 2) == 9.49
    assert hub.counts()["online_now"] == 4

    # Ablauf: Warnung 15 min vorher, dann zurück auf Notbetrieb
    async_fire_time_changed(hass, restore - timedelta(minutes=14))
    await hass.async_block_till_done()
    assert any("endet bald" in n.data["title"] for n in notes)
    async_fire_time_changed(hass, restore + timedelta(seconds=1))
    await hass.async_block_till_done()
    assert hub.mode == "emergency"
    assert unifi.route_targets()[1] == ["aa:00:00:00:00:03", "aa:00:00:00:00:05", "net:guest"]

    # Abgelaufene Tagesflat lässt sich nicht freischalten
    from custom_components.homelines.hub import FlatError
    try:
        await hub.async_activate_flat(dt_util.utcnow() - timedelta(hours=25))
        raise AssertionError("FlatError erwartet")
    except FlatError as err:
        assert err.args[0] == "flat_expired"

    # Hauptleitung zurück
    hass.states.async_set("sensor.unifi_active_wan_id", "WAN2")
    await hass.async_block_till_done()
    assert hub.mode == "normal"
    assert any("wieder da" in n.data["title"] for n in notes)
    assert sw_on and sw_on[-1].data["entity_id"] == "switch.unifi_wan_auto_speedtest"
    assert hub.data["history"]["emergencies"]


async def test_planned_reconnect_is_silent(hass, unifi, ping):
    notes = async_mock_service(hass, "notify", "mobile_app_mein_handy")
    entry, hub = await _setup(hass)
    hub._planned_until = dt_util.utcnow() + timedelta(minutes=3)
    hass.states.async_set("sensor.unifi_active_wan_id", "WAN3")
    await hass.async_block_till_done()
    assert hub.mode == "emergency" and hub.snapshot()["planned"]
    hass.states.async_set("sensor.unifi_active_wan_id", "WAN2")
    await hass.async_block_till_done()
    assert hub.mode == "normal"
    assert notes == []


async def test_reconnect_and_entities(hass, unifi, ping):
    async def fake(self, method, iface):
        return "ok_same_ip", "203.0.113.7", "203.0.113.7"

    data = {**BASE, "reconnect_enabled": True, "ssh_host": "192.168.1.1", "ssh_port": 22, "ssh_user": "root",
            "ssh_password": "pw", "ppp_interface": "ppp1", "reconnect_method": "pppd_hup", "reconnect_time": "04:00:00"}
    with patch("custom_components.homelines.config_flow.UnifiAdapter"):
        pass
    entry = MockConfigEntry(domain=DOMAIN, title="HomeLines", data=data, options=OPTIONS)
    entry.add_to_hass(hass)
    hass.states.async_set("sensor.unifi_active_wan_id", "WAN2")
    with patch("custom_components.homelines.reconnect.SSHClient.reconnect", fake):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        await hass.services.async_call("button", "press", {"entity_id": "button.homelines_reconnect_now"}
                                       if hass.states.get("button.homelines_reconnect_now")
                                       else {"entity_id": "button.homelines_reconnect_now"}, blocking=True)
        await hass.async_block_till_done()
    hub = hass.data[DOMAIN][entry.entry_id]
    assert hub.data["reconnect"]["result"] == "ok_same_ip"
    from homeassistant.helpers import entity_registry as er
    ids = [e.unique_id for e in er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)]
    for needle in ("availability_7d", "outages_24h", "outages_7d", "outages_30d", "downtime_7d", "latency",
                   "packet_loss", "last_outage", "wan_ip", "last_reconnect", "reconnect_result", "cost",
                   "balance", "usage", "restore_at", "dayflat_end", "devices_online", "active_wan"):
        assert any(needle in i for i in ids), needle
    assert any(i.endswith("daily_reconnect") for i in ids)
    assert any(i.endswith("reconnect_time") for i in ids)


async def test_outage_log(hass, unifi, ping):
    entry, hub = await _setup(hass)
    events = []
    hass.bus.async_listen("homelines_outage_ended", lambda e: events.append(e))
    ping["up"] = False
    await hub._async_ping()
    await hub._async_ping()
    assert hub.internet is False and hub.log.current
    ping["up"] = True
    await hub._async_ping()
    await hass.async_block_till_done()
    assert hub.internet is True and len(hub.log.outages) == 1 and events
    assert hub.outage_stats()["outages_24h"] == 1
    assert hass.states.get("binary_sensor.homelines_internet").state == "on"


async def test_websocket(hass, unifi, ping, hass_ws_client):
    entry, hub = await _setup(hass)
    client = await hass_ws_client(hass)
    await client.send_json({"id": 1, "type": "homelines/subscribe"})
    res = await client.receive_json()
    assert res["success"]
    ev = await client.receive_json()
    snap = ev["event"]
    assert snap["mode"] == "normal" and snap["devices"] and snap["wans"]
    assert {w["id"] for w in snap["wans"]} >= {"WAN2", "WAN3"}
    await client.send_json({"id": 2, "type": "homelines/activate_dayflat"})
    res = await client.receive_json()
    while res.get("type") == "event":
        res = await client.receive_json()
    assert not res["success"] and res["error"]["code"] == "not_in_emergency"
    await client.send_json({"id": 3, "type": "homelines/set_group", "kind": "network", "target": "iot", "group": "always"})
    res = await client.receive_json()
    while res.get("type") == "event":
        res = await client.receive_json()
    assert res["success"]
    assert hub.data["groups"]["networks"]["iot"] == "always"


async def test_unload_and_remove(hass, unifi, ping):
    entry, hub = await _setup(hass)
    assert unifi.routes
    assert await hass.config_entries.async_remove(entry.entry_id)
    await hass.async_block_till_done()
    assert unifi.routes == []


async def test_home_assistant_is_protected(hass, unifi, ping):
    with patch("homeassistant.components.network.async_get_source_ip", return_value="192.168.1.10"):
        entry, hub = await _setup(hass)
        await hub._async_refresh_inventory()
    assert hub.data["groups"]["devices"]["aa:00:00:00:00:01"] == "always"
    assert "aa:00:00:00:00:01" not in unifi.route_targets()[1]


async def test_notify_targets_and_routing(hass, unifi, ping):
    entry, hub = await _setup(hass, options={})
    sms = async_mock_service(hass, "notify", "sms_gateway")
    push = async_mock_service(hass, "notify", "mobile_app_mein_handy")
    hass.states.async_set("notify.smtp_alex", "unknown")
    mail = async_mock_service(hass, "notify", "send_message")

    async def add(label, service, recipient="", is_sms=False):
        r = await hass.config_entries.options.async_init(entry.entry_id)
        r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "notify"})
        assert r["type"] is FlowResultType.MENU
        r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "notify_add"})
        r = await hass.config_entries.options.async_configure(
            r["flow_id"], {"label": label, "service": service, "recipient": recipient, "sms": is_sms})
        assert r["type"] is FlowResultType.CREATE_ENTRY
        await hass.async_block_till_done()

    await add("Push Handy", "notify.mobile_app_mein_handy")
    await add("SMS Alex", "notify.sms_gateway", "+491230000001, +491230000002", True)
    await add("Mail Alex", "notify.smtp_alex")
    targets = hass.config_entries.async_get_entry(entry.entry_id).options["notify_targets"]
    ids = {t["label"]: t["id"] for t in targets}

    # Neueinwahl-Fehler nur per Mail, Notbetrieb per Push und SMS, Handy-Meldung aus
    r = await hass.config_entries.options.async_init(entry.entry_id)
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "notify"})
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "notify_messages"})
    r = await hass.config_entries.options.async_configure(r["flow_id"], {
        "emergency": [ids["Push Handy"], ids["SMS Alex"]], "flat_warning": [ids["Push Handy"]],
        "flat_expired": [ids["Push Handy"]], "restored": [ids["Push Handy"], ids["SMS Alex"]],
        "backup_down": [ids["Push Handy"]], "phone_silent": [], "reconnect_failed": [ids["Mail Alex"]],
        "backup_down_minutes": 10})
    assert r["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    hub = hass.data[DOMAIN][entry.entry_id]

    hass.states.async_set("sensor.unifi_active_wan_id", "WAN3")
    await hass.async_block_till_done()
    assert len(push) == 1 and push[0].data["title"].startswith("Internet: Notbetrieb")
    assert len(sms) == 1
    assert sms[0].data["target"] == ["+491230000001", "+491230000002"]
    assert "title" not in sms[0].data and sms[0].data["message"].startswith("Internet: Notbetrieb")
    assert mail == []

    await hub.notify("reconnect_failed", "Internet: Neueinwahl fehlgeschlagen", "Fehler")
    assert len(mail) == 1 and mail[0].data["entity_id"] == "notify.smtp_alex"
    assert len(push) == 1 and len(sms) == 1

    # Empfänger löschen
    r = await hass.config_entries.options.async_init(entry.entry_id)
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "notify"})
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "notify_pick"})
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"target": ids["SMS Alex"]})
    r = await hass.config_entries.options.async_configure(r["flow_id"], {
        "label": "SMS Alex", "service": "notify.sms_gateway", "recipient": "", "sms": True, "remove": True})
    assert r["type"] is FlowResultType.CREATE_ENTRY
    opts = hass.config_entries.async_get_entry(entry.entry_id).options
    assert len(opts["notify_targets"]) == 2
    assert ids["SMS Alex"] not in opts["notify_routes"]["emergency"]


async def test_backup_down_watch(hass, unifi, ping, freezer):
    notes = async_mock_service(hass, "notify", "mobile_app_mein_handy")
    entry, hub = await _setup(hass)
    now = dt_util.utcnow()
    freezer.move_to(now + timedelta(minutes=1))
    async_fire_time_changed(hass, now + timedelta(minutes=1))
    await hass.async_block_till_done()
    assert not any("Backup" in n.data["title"] for n in notes)
    freezer.move_to(now + timedelta(minutes=12))
    async_fire_time_changed(hass, now + timedelta(minutes=12))
    await hass.async_block_till_done()
    assert sum("Backup-Leitung ausgefallen" in n.data["title"] for n in notes) == 1
    freezer.move_to(now + timedelta(minutes=20))
    async_fire_time_changed(hass, now + timedelta(minutes=20))
    await hass.async_block_till_done()
    assert sum("Backup-Leitung ausgefallen" in n.data["title"] for n in notes) == 1  # nur einmal
    hass.states.async_set("binary_sensor.unifi_wan3_internet", "on")
    freezer.move_to(now + timedelta(minutes=22))
    async_fire_time_changed(hass, now + timedelta(minutes=22))
    await hass.async_block_till_done()
    assert any("wieder bereit" in n.data["title"] for n in notes)


async def test_test_notify_button(hass, unifi, ping):
    entry, hub = await _setup(hass)
    notes = async_mock_service(hass, "notify", "mobile_app_mein_handy")
    await hass.services.async_call(DOMAIN, "test_notify", {}, blocking=True)
    assert notes and "Testmeldung" in notes[0].data["title"]


COLD = {**OPTIONS, "standby": "cold", "detection": "monitor", "router_ip": "192.168.1.1", "detect_delay": 60,
        "phone_wifi": "sensor.notfall_handy_wifi"}


async def test_cold_standby_assistant(hass, unifi, ping, freezer):
    hass.states.async_set("sensor.notfall_handy_wifi", "MeinWLAN")
    hass.states.async_set("binary_sensor.notfall_handy_mobile_data", "off")
    notes = async_mock_service(hass, "notify", "mobile_app_mein_handy")
    entry, hub = await _setup(hass, options=COLD)
    hass.states.async_set("binary_sensor.notfall_handy_mobile_data", "off")
    await hass.async_block_till_done()
    t0 = dt_util.utcnow()

    # Kalte Bereitschaft: WAN3 offline ist normal, kein Backup-Alarm
    freezer.move_to(t0 + timedelta(minutes=15))
    async_fire_time_changed(hass, t0 + timedelta(minutes=15))
    await hass.async_block_till_done()
    assert not any("Backup" in n.data["title"] for n in notes)

    # DSL fällt aus: Router antwortet, Internet nicht
    ping["up"] = False

    async def router_ok(self, host, count, timeout=2):
        from custom_components.homelines.monitor import PingResult
        up = host == "192.168.1.1" or ping["up"]
        return PingResult(host, up, 1.0 if up else None, 0.0 if up else 100.0)

    with patch("custom_components.homelines.monitor.Pinger.ping", router_ok):
        await hub._async_ping()
        await hub._async_ping()
        assert hub.mode == "normal" and hub.snapshot()["pending_since"]  # wartet die 60 s ab
        freezer.move_to(t0 + timedelta(minutes=16, seconds=5))
        async_fire_time_changed(hass, t0 + timedelta(minutes=16, seconds=5))
        await hass.async_block_till_done()
        assert hub.mode == "emergency"
        assert any(n.data["title"] == "Internet: Hauptleitung ausgefallen" for n in notes)
        steps = {s["key"]: s["done"] for s in hub.assistant()["steps"]}
        assert steps == {"book": False, "wifi_off": False, "data_on": False, "usb": True, "tether": False}

        # Schritte am Handy erledigen, Tethering läuft (WAN3 online), Internet wieder da
        hass.states.async_set("sensor.notfall_handy_wifi", "<not connected>")
        hass.states.async_set("binary_sensor.notfall_handy_mobile_data", "on")
        hass.states.async_set("binary_sensor.unifi_wan3_internet", "on")
        await hass.async_block_till_done()
        ping["up"] = True
        await hub._async_ping()
        await hass.async_block_till_done()
        assert hub.mode == "emergency"  # läuft über Mobilfunk, Hauptleitung noch weg
        steps = {s["key"]: s["done"] for s in hub.assistant()["steps"]}
        assert steps["wifi_off"] and steps["data_on"] and steps["tether"]
        await hub.async_activate_flat()
        assert hub.mode == "dayflat"

        # DSL zurück: Tethering aus -> Internet über DSL
        hass.states.async_set("binary_sensor.unifi_wan3_internet", "off")
        await hass.async_block_till_done()
        await hub._async_ping()
        await hass.async_block_till_done()
    assert hub.mode == "normal"
    restored = [n for n in notes if n.data["title"] == "Internet: Hauptleitung wieder da"]
    assert restored and "zurückstellen" in restored[0].data["message"]
    a = hub.assistant()
    assert a["kind"] == "return"
    hass.states.async_set("binary_sensor.notfall_handy_mobile_data", "off")
    hass.states.async_set("sensor.notfall_handy_wifi", "MeinWLAN")
    await hass.async_block_till_done()
    assert hub.assistant() is None


async def test_fritz_style_switches(hass, ping):
    hass.states.async_set("binary_sensor.fritz_connection", "on")
    for n in ("tv", "laptop", "ha"):
        hass.states.async_set(f"switch.fritz_{n}_internet", "on", {"friendly_name": f"{n} Internet"})
    data = {"router_type": "switches",
            "switch_entities": ["switch.fritz_tv_internet", "switch.fritz_laptop_internet", "switch.fritz_ha_internet"],
            "detection": "primary_off", "primary_status_entity": "binary_sensor.fritz_connection",
            "backup_wan": "WAN2", "reconnect_enabled": False}
    entry = MockConfigEntry(domain=DOMAIN, title="HomeLines", data=data, options={})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    hub = hass.data[DOMAIN][entry.entry_id]
    off = async_mock_service(hass, "switch", "turn_off")
    on = async_mock_service(hass, "switch", "turn_on")
    await hub.async_set_group("device", "switch.fritz_ha_internet", "always")
    await hub.async_set_group("device", "switch.fritz_tv_internet", "never")
    assert off == []  # im Normalbetrieb wird nichts gesperrt
    hass.states.async_set("binary_sensor.fritz_connection", "off")
    await hass.async_block_till_done()
    assert hub.mode == "emergency"
    assert sorted(c.data["entity_id"] for c in off) == ["switch.fritz_laptop_internet", "switch.fritz_tv_internet"]
    for c in off:
        hass.states.async_set(c.data["entity_id"], "off")
    await hub.async_activate_flat()
    assert any(c.data["entity_id"] == "switch.fritz_laptop_internet" for c in on)
    hass.states.async_set("switch.fritz_laptop_internet", "on")
    hass.states.async_set("binary_sensor.fritz_connection", "on")
    await hass.async_block_till_done()
    assert hub.mode == "normal"
    assert any(c.data["entity_id"] == "switch.fritz_tv_internet" for c in on)


async def test_reconnect_via_ha_button(hass, ping):
    hass.states.async_set("sensor.fritz_external_ip", "203.0.113.8")
    hass.states.async_set("button.fritz_reconnect", "unknown")

    async def press(call):
        hass.states.async_set("sensor.fritz_external_ip", "198.51.100.9")

    data = {"router_type": "none", "detection": "monitor", "reconnect_enabled": True,
            "reconnect_method": "ha_action", "reconnect_entity": "button.fritz_reconnect",
            "wan_ip_entity": "sensor.fritz_external_ip", "reconnect_time": "04:00:00"}
    entry = MockConfigEntry(domain=DOMAIN, title="HomeLines", data=data, options={})
    entry.add_to_hass(hass)
    with patch("custom_components.homelines.hub.RECONNECT_POLL", 0.01), \
            patch("custom_components.homelines.hub.RECONNECT_WAIT", 2):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        hass.services.async_register("button", "press", press)
        hub = hass.data[DOMAIN][entry.entry_id]
        assert hub.reconnect_configured and hub.reconnect_enabled
        assert await hub.async_reconnect() == "ok_new_ip"
    assert hub.data["reconnect"]["ip"] == "198.51.100.9"


async def test_units_and_local_channels(hass, unifi, ping):
    entry, hub = await _setup(hass)
    hass.states.async_set("sensor.notfall_handy_mobile_rx_gb", "100", {"unit_of_measurement": "MB"})
    hass.states.async_set("sensor.notfall_handy_mobile_tx_gb", "0", {"unit_of_measurement": "MB"})
    await hass.async_block_till_done()
    assert hub._phone_total_mb() == 100
    scripts = async_mock_service(hass, "script", "turn_on")
    pn = async_mock_service(hass, "persistent_notification", "create")
    await hub._send({"service": "script.ansage", "recipient": "", "sms": False}, "T", "M")
    await hub._send({"service": "persistent_notification.create", "recipient": "", "sms": False}, "T", "M")
    assert scripts[0].data["variables"]["message"] == "M"
    assert pn[0].data["title"] == "T"


async def test_fixed_entity_ids(hass, unifi, ping):
    from homeassistant.helpers import entity_registry as er
    entry, hub = await _setup(hass)
    for eid in ("binary_sensor.homelines_internet", "sensor.homelines_outages_24h", "sensor.homelines_outages_7d",
                "sensor.homelines_availability_7d", "sensor.homelines_downtime_7d", "sensor.homelines_latency",
                "sensor.homelines_packet_loss", "sensor.homelines_last_outage", "sensor.homelines_last_outage_duration",
                "sensor.homelines_last_check", "sensor.homelines_status", "button.homelines_test_notify"):
        assert hass.states.get(eid) is not None, eid
    assert hass.states.get("sensor.homelines_last_check").state not in ("unknown", "unavailable")
    # Migration: eine alte, sprachabhängige ID wird beim nächsten Start auf die feste umgestellt
    reg = er.async_get(hass)
    reg.async_update_entity("sensor.homelines_outages_24h", new_entity_id="sensor.homelines_ausfalle_24_h")
    hub.data.pop("ids_fixed")
    await hub._store.async_save(hub._stored())
    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    assert reg.async_get("sensor.homelines_outages_24h") is not None
    assert hass.states.get("sensor.homelines_outages_24h") is not None


async def test_wan_names_with_ip_and_router_default(hass, unifi, ping):
    from custom_components.homelines.hub import _wan_id
    assert _wan_id("binary_sensor.unifi_wan_192_168_1_1_default_unifi_wan3_internet") == "WAN3"
    assert _wan_id("UniFi WAN (192.168.1.1 / default) UniFi WAN3 Internet") == "WAN3"
    assert _wan_id("WAN2 (Port 3 DSL)") == "WAN2"
    assert _wan_id("WAN") == "WAN1"
    hass.states.async_set("sensor.unifi_active_wan_id", "WAN2")
    hass.states.async_set("binary_sensor.unifi_wan_192_168_1_1_default_unifi_wan3_internet", "off",
                          {"friendly_name": "UniFi WAN (192.168.1.1 / default) UniFi WAN3 Internet"})
    data = {**BASE, "wan_status_entities": ["binary_sensor.unifi_wan_192_168_1_1_default_unifi_wan3_internet"]}
    entry = MockConfigEntry(domain=DOMAIN, title="HomeLines", data=data, options={})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    hub = hass.data[DOMAIN][entry.entry_id]
    lines = {l["id"]: l for l in hub.wan_lines()}
    assert set(lines) == {"WAN1", "WAN2", "WAN3"}
    assert lines["WAN3"]["name"] == "5G Backup" and lines["WAN3"]["state"] == "offline"
    assert lines["WAN1"]["name"] == "Internet 1"
    assert hub.router_ip == "192.168.1.1"
    assert hass.states.get("binary_sensor.homelines_router") is not None


async def test_switching_usage_sensors_does_not_count(hass, unifi, ping):
    hass.states.async_set("sensor.notfall_handy_total_rx_gb", "2.11")
    entry, hub = await _setup(hass, options={**OPTIONS, "phone_rx": "sensor.notfall_handy_total_rx_gb"})
    hass.states.async_set("sensor.notfall_handy_total_rx_gb", "2.20")
    await hass.async_block_till_done()
    assert hub.data["usage"]["mb"] > 0
    await hub.async_reset_usage(20.0)
    hass.config_entries.async_update_entry(entry, options={**OPTIONS})  # zurück auf Mobile Rx
    await hass.async_block_till_done()
    hub = hass.data[DOMAIN][entry.entry_id]
    assert hub.data["usage"]["mb"] == 0 and hub.data["usage"]["cost"] == 0
    hass.states.async_set("sensor.notfall_handy_mobile_rx_gb", str(0.032 + 10 / 1024))
    await hass.async_block_till_done()
    assert round(hub.data["usage"]["mb"]) == 10 and round(hub.data["usage"]["cost"], 2) == 0.30


async def test_phone_wake_and_device_heartbeat(hass, unifi, ping, freezer):
    """Weckruf nur bei Stille, Lebenszeichen von jeder Entität des Handy-Geräts."""
    from homeassistant.helpers import device_registry as dr, entity_registry as er

    app = MockConfigEntry(domain="mobile_app", title="notfall_handy")
    app.add_to_hass(hass)
    dev = dr.async_get(hass).async_get_or_create(config_entry_id=app.entry_id, identifiers={("mobile_app", "notfall_handy")})
    ereg = er.async_get(hass)
    for obj in ("notfall_handy_battery", "notfall_handy_wifi_signal"):
        ereg.async_get_or_create("sensor", "mobile_app", obj, suggested_object_id=obj, device_id=dev.id)
    wake = async_mock_service(hass, "notify", "mobile_app_notfall_handy")
    t0 = dt_util.utcnow()
    entry, hub = await _setup(hass, options={**OPTIONS, "phone_notify": "notify.mobile_app_notfall_handy",
                                              "phone_wake_minutes": 10})
    assert "sensor.notfall_handy_wifi_signal" in hub._phone_device_entities()

    async def tick(minutes):
        freezer.move_to(t0 + timedelta(minutes=minutes))
        async_fire_time_changed(hass, t0 + timedelta(minutes=minutes))
        await hass.async_block_till_done()

    await tick(5)
    assert not wake
    # nur das WLAN-Signal meldet sich – das zählt als Lebenszeichen
    hass.states.async_set("sensor.notfall_handy_wifi_signal", "-55")
    await tick(12)
    assert not wake
    await tick(18)  # 13 min still
    assert len(wake) == 1 and wake[0].data["message"] == "command_update_sensors"
    assert hub.phone()["woken_at"]
    await tick(24)  # kein erneuter Weckruf innerhalb von 10 min
    assert len(wake) == 1
    await tick(29)
    assert len(wake) == 2
    # Notbetrieb weckt sofort
    hass.states.async_set("sensor.notfall_handy_wifi_signal", "-56")
    hass.states.async_set("sensor.unifi_active_wan_id", "WAN3")
    hass.states.async_set("binary_sensor.unifi_wan2_internet", "off")
    await hass.async_block_till_done()
    assert hub.mode == "emergency"
    assert len(wake) == 3


async def test_options_phone_wake(hass, unifi, ping):
    async_mock_service(hass, "notify", "mobile_app_notfall_handy")
    entry, _ = await _setup(hass)
    r = await hass.config_entries.options.async_init(entry.entry_id)
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "phone"})
    assert r["type"] is FlowResultType.FORM
    opts = r["data_schema"].schema
    key = next(k for k in opts if str(k) == "phone_notify")
    assert "notify.mobile_app_notfall_handy" in opts[key].config["options"]
    r = await hass.config_entries.options.async_configure(r["flow_id"], {
        **{k: v for k, v in OPTIONS.items() if k.startswith("phone_")},
        "phone_notify": "notify.mobile_app_notfall_handy", "phone_wake_minutes": 15, "phone_stale_minutes": 30})
    assert r["type"] is FlowResultType.CREATE_ENTRY
    assert entry.options["phone_notify"] == "notify.mobile_app_notfall_handy"
    assert entry.options["phone_wake_minutes"] == 15


def test_reconnect_command_and_exit_code():
    import asyncio
    from custom_components.homelines.reconnect import LinkState, SSHClient, SSHError, build_command

    cmd = build_command("pppd_hup", "ppp1")
    assert "killall" not in cmd and "pidof pppd" in cmd and "kill -HUP" in cmd

    class Fake(SSHClient):
        async def link_state(self, iface):
            return LinkState("203.0.113.8", "7")

        async def run(self, command, timeout=30):
            return 127, "sh: killall: not found"

    import pytest
    with pytest.raises(SSHError, match="127"):
        asyncio.run(Fake("h", 22, "root", "x").reconnect("pppd_hup", "ppp1"))


async def test_usage_ignores_missing_counter(hass, unifi, ping):
    """Fehlt Tx kurz (Neustart), darf das nicht als Verbrauch zählen."""
    entry, hub = await _setup(hass)
    hass.states.async_set("sensor.notfall_handy_mobile_tx_gb", "unavailable")
    await hass.async_block_till_done()
    hass.states.async_set("sensor.notfall_handy_mobile_tx_gb", "0.007")
    await hass.async_block_till_done()
    hass.states.async_set("sensor.notfall_handy_mobile_rx_gb", "unknown")
    hass.states.async_set("sensor.notfall_handy_mobile_rx_gb", "0.032")
    await hass.async_block_till_done()
    assert hub.data["usage"]["mb"] == 0
    # echter Verbrauch zählt weiter
    hass.states.async_set("sensor.notfall_handy_mobile_rx_gb", "0.034")
    await hass.async_block_till_done()
    assert round(hub.data["usage"]["mb"]) == 2
    # Handy-Neustart: Zähler beginnt bei fast null
    hass.states.async_set("sensor.notfall_handy_mobile_rx_gb", "0.001")
    hass.states.async_set("sensor.notfall_handy_mobile_tx_gb", "0.0")
    await hass.async_block_till_done()
    assert 2 < hub.data["usage"]["mb"] < 4
