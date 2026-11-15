"""0.7.0: UniFi vergibt neue IDs (WAN, Netze) und Umstieg von LineGuard."""

from __future__ import annotations

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntryState
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import issue_registry as ir
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.homelines.const import DOMAIN

from test_homelines import BASE, OPTIONS, _setup


async def _refresh(hass, hub):
    await hub._async_refresh_inventory()
    await hass.async_block_till_done()


async def test_wan_and_network_get_new_ids(hass, unifi, ping):
    entry, hub = await _setup(hass)
    await hub.async_set_group("network", "guest", "never")
    assert unifi.routes[0]["network_id"] == "wan2"
    assert "net:guest" in unifi.route_targets()[1]

    # UniFi legt WAN2 und das Gäste-Netz neu an
    unifi.recreate("wan2", "wan2-neu")
    unifi.recreate("guest", "guest-neu")
    await _refresh(hass, hub)

    assert hub.router_error is None
    assert unifi.routes[0]["network_id"] == "wan2-neu"
    assert "net:guest-neu" in unifi.route_targets()[1]
    assert hub.data["groups"]["networks"] == {"guest-neu": "never"}
    assert not ir.async_get(hass).async_get_issue(DOMAIN, f"primary_wan_missing_{entry.entry_id}")


async def test_stale_inventory_is_retried(hass, unifi, ping):
    """Regel schlägt mit InvalidNetworkConfId fehl → neu abgleichen und noch einmal setzen."""
    _, hub = await _setup(hass)
    unifi.recreate("wan2", "wan2-neu")  # Hub kennt das noch nicht
    await hub.async_set_group("device", "aa:00:00:00:00:03", "always")
    assert hub.router_error is None
    assert unifi.routes[0]["network_id"] == "wan2-neu"


async def test_wan_gone_gives_clear_notice(hass, unifi, ping):
    entry, hub = await _setup(hass)
    calls = len(unifi.calls)
    unifi.networks = [n for n in unifi.networks if n["_id"] != "wan2"]
    await _refresh(hass, hub)

    assert hub.wan_missing == "DSL"
    assert "nicht mehr gefunden" in hub.router_error and "HTTP" not in hub.router_error
    assert not [c for c in unifi.calls[calls:] if c[0] in ("PUT", "POST")]
    issue = ir.async_get(hass).async_get_issue(DOMAIN, f"primary_wan_missing_{entry.entry_id}")
    assert issue and issue.translation_placeholders == {"name": "DSL"}
    assert hub.snapshot()["wan_missing"] == "DSL"

    # Leitung in den Optionen neu wählen → Hinweis weg
    hass.config_entries.async_update_entry(entry, options={**entry.options, "primary_wan_network": "wan1"})
    await hass.async_block_till_done()
    hub = hass.data[DOMAIN][entry.entry_id]
    await _refresh(hass, hub)
    assert hub.wan_missing is None and hub.router_error is None
    assert not ir.async_get(hass).async_get_issue(DOMAIN, f"primary_wan_missing_{entry.entry_id}")


async def test_unknown_network_is_marked_not_sent(hass, unifi, ping):
    _, hub = await _setup(hass)
    await hub.async_set_group("network", "guest", "never")
    await hub.async_set_group("network", "iot", "never")
    unifi.networks = [n for n in unifi.networks if n["_id"] != "guest"]
    unifi.online = [c for c in unifi.online if c.get("network") != "Gäste"]
    await _refresh(hass, hub)

    assert hub.router_error is None
    targets = unifi.route_targets()[1]
    assert "net:iot" in targets and "net:guest" not in targets
    missing = [n for n in hub.snapshot()["networks"] if n.get("missing")]
    assert missing == [{"id": "guest", "name": "Gäste", "group": "never", "missing": True}]
    # In der Karte „Entfernen“ = Gruppe erben
    await hub.async_set_group("network", "guest", None)
    assert not [n for n in hub.snapshot()["networks"] if n.get("missing")]


def _legacy_store(hass_storage, entry_id):
    hass_storage[f"lineguard.{entry_id}"] = {"version": 1, "minor_version": 1, "key": f"lineguard.{entry_id}", "data": {
        "groups": {"devices": {"aa:00:00:00:00:02": "always"}, "networks": {"guest": "never"}},
        "usage": {"reset_at": "2026-10-01T00:00:00+00:00", "mb": 12.5, "cost": 0.38, "last_total": None,
                  "flats": 1, "start_balance": 20.0},
        "history": {"emergencies": [{"start": "2026-10-02T10:00:00+00:00", "end": "2026-10-02T11:00:00+00:00"}]},
        "ids_fixed": True,
    }}


async def test_take_over_from_lineguard(hass, unifi, ping, hass_storage):
    old = MockConfigEntry(domain="lineguard", title="LineGuard", data=BASE, options=OPTIONS,
                          unique_id="unifi_192.168.1.1")
    old.add_to_hass(hass)
    _legacy_store(hass_storage, old.entry_id)
    unifi.routes.append({"_id": "alt", "description": "LineGuard Notbetrieb", "network_id": "wan2",
                         "target_devices": [{"type": "ALL_CLIENTS"}], "enabled": False})

    r = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert r["type"] is FlowResultType.MENU and r["step_id"] == "legacy"
    r = await hass.config_entries.flow.async_configure(r["flow_id"], {"next_step_id": "import_legacy"})
    assert r["type"] is FlowResultType.CREATE_ENTRY
    assert r["title"] == "HomeLines" and r["data"]["imported_from"] == old.entry_id
    await hass.async_block_till_done()

    entry = hass.config_entries.async_entries(DOMAIN)[0]
    hub = hass.data[DOMAIN][entry.entry_id]
    assert hub.data["groups"]["networks"] == {"guest": "never"}
    assert hub.data["usage"]["flats"] == 1 and hub.data["usage"]["start_balance"] == 20.0
    assert len(hub.data["history"]["emergencies"]) == 1
    # alte Regel weg (LineGuard läuft nicht), eigene Regel da
    descs = [x["description"] for x in unifi.routes]
    assert "LineGuard Notbetrieb" not in descs and "HomeLines Notbetrieb" in descs
    assert hass.states.get("sensor.homelines_status") is not None

    # Kein zweites Angebot zur Übernahme
    r = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert r["type"] is FlowResultType.FORM and r["step_id"] == "user"


async def test_lineguard_still_running_gives_notice(hass, unifi, ping, hass_storage):
    old = MockConfigEntry(domain="lineguard", title="Mein Netz", data=BASE, options=OPTIONS)
    old.add_to_hass(hass)
    old.mock_state(hass, ConfigEntryState.LOADED)
    _legacy_store(hass_storage, old.entry_id)
    unifi.routes.append({"_id": "alt", "description": "LineGuard Notbetrieb", "network_id": "wan2",
                         "target_devices": [{"type": "ALL_CLIENTS"}], "enabled": False})

    r = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    r = await hass.config_entries.flow.async_configure(r["flow_id"], {"next_step_id": "import_legacy"})
    assert r["title"] == "Mein Netz"
    await hass.async_block_till_done()
    entry = hass.config_entries.async_entries(DOMAIN)[0]
    hub = hass.data[DOMAIN][entry.entry_id]
    assert ir.async_get(hass).async_get_issue(DOMAIN, f"legacy_running_{entry.entry_id}")
    assert "LineGuard Notbetrieb" in [x["description"] for x in unifi.routes]

    # LineGuard entfernt → Hinweis weg, alte Regel gelöscht
    old.mock_state(hass, ConfigEntryState.NOT_LOADED)
    await _refresh(hass, hub)
    assert not ir.async_get(hass).async_get_issue(DOMAIN, f"legacy_running_{entry.entry_id}")
    assert "LineGuard Notbetrieb" not in [x["description"] for x in unifi.routes]
    assert hub.data["legacy"]["route_removed"] is True


async def test_flow_saves_wan_label(hass, unifi, ping):
    entry, _ = await _setup(hass)
    r = await hass.config_entries.options.async_init(entry.entry_id)
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "lines"})
    defaults = {str(k): k.default() for k in r["data_schema"].schema if hasattr(k, "default") and callable(k.default)}
    r = await hass.config_entries.options.async_configure(r["flow_id"], {**{k: v for k, v in defaults.items()},
                                                                        "primary_wan_network": "wan2"})
    assert entry.options["primary_wan_label"] == {"name": "DSL", "group": "WAN2"}
