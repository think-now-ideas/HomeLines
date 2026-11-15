"""0.7.1: grafische Editoren der Karten (ha-form) und zentrale Leitungsnamen.

Die Editoren laufen in Chromium (Playwright) mit einem nachgebauten ``ha-form``, der Schema und Daten
festhält und Änderungen wie das echte Element meldet (alte Daten + geänderte Felder).
Ohne Playwright werden die Browser-Tests übersprungen.
"""
import json
from pathlib import Path

import pytest

from test_homelines import OPTIONS, _setup

CARD = Path(__file__).parent.parent / "custom_components" / "homelines" / "www" / "homelines-card.js"

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script>
customElements.define("ha-icon", class extends HTMLElement {});
customElements.define("ha-card", class extends HTMLElement {});
customElements.define("ha-form", class extends HTMLElement {
  emit(change) { this.dispatchEvent(new CustomEvent("value-changed", { detail: { value: { ...this.data, ...change } } })); }
});
</script>
<script>%CARD%</script></head><body>
<script>
window.HASS = { states: { "sensor.homelines_active_wan": { state: "WAN2", attributes: { name: "DSL",
  lines: [{ id: "WAN1", name: "Glasfaser" }, { id: "WAN2", name: "DSL" }, { id: "WAN3", name: "5G Backup" }] } } },
  connection: { subscribeMessage: async () => () => {}, sendMessagePromise: async () => ({}) } };
window.edit = (type, cfg) => {
  const el = customElements.get(type).getConfigElement();
  window.OUT = []; el.addEventListener("config-changed", e => OUT.push(e.detail.config));
  el.setConfig(cfg); el.hass = HASS; document.body.appendChild(el); window.ED = el;
  const f = el.querySelector("ha-form");
  const keys = (s) => s.flatMap(x => x.type === "expandable" ? [x.name || "", ...keys(x.schema).map(k => (x.name ? x.name + "." : "") + k)] : [x.name]);
  return { keys: keys(f.schema).filter(Boolean), data: f.data };
};
window.change = (v) => { ED.querySelector("ha-form").emit(v); return OUT[OUT.length - 1]; };
</script></body></html>"""


@pytest.fixture
def page():
    pw = pytest.importorskip("playwright.sync_api")
    with pw.sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.set_content(PAGE.replace("%CARD%", CARD.read_text(encoding="utf-8")))
        yield pg
        assert not errors, errors
        browser.close()


def test_mini_editor_keeps_unknown_keys(page):
    cfg = {"type": "custom:homelines-mini", "layout": "tile", "name": "Internet", "popup_view": "/x/internet",
           "popup_cards": [{"type": "custom:homelines-tile", "name": "DSL"}], "grid_options": {"columns": 12}}
    r = page.evaluate("([t, c]) => edit(t, c)", ["homelines-mini", cfg])
    assert {"layout", "name", "throughput_entity", "upload_entity", "throughput_hours", "info",
            "navigation_path", "popup_view", "popup_columns", "popup_show_card"} <= set(r["keys"])
    assert r["data"]["popup_view"] == "/x/internet"
    out = page.evaluate("(v) => change(v)", {"throughput_entity": "sensor.wan_download", "popup_view": ""})
    assert out["type"] == "custom:homelines-mini"
    assert out["throughput_entity"] == "sensor.wan_download"
    assert "popup_view" not in out  # geleert → entfernt
    assert out["popup_cards"] == cfg["popup_cards"] and out["grid_options"] == {"columns": 12}


def test_card_editor_lines_from_integration(page):
    cfg = {"type": "custom:homelines-card", "lines": {"WAN2": {"name": "DSL", "full_width": True}}}
    r = page.evaluate("([t, c]) => edit(t, c)", ["homelines-card", cfg])
    assert {"lines.WAN1.name", "lines.WAN2.tap", "lines.WAN3.info", "title", "compact"} <= set(r["keys"])
    # verschachtelte Abschnitte bekommen immer ein Objekt (ha-form greift sonst ins Leere)
    assert r["data"]["lines"] == {"WAN1": {}, "WAN2": {"name": "DSL", "full_width": True}, "WAN3": {}}
    out = page.evaluate("(v) => change(v)", {"compact": True, "lines": {"WAN2": {"name": "", "full_width": True},
                                                                         "WAN3": {"tap": "#notfall"}, "WAN1": {}}})
    assert out == {"type": "custom:homelines-card", "compact": True,
                   "lines": {"WAN2": {"full_width": True}, "WAN3": {"tap": "#notfall"}}}


def test_tile_editor(page):
    r = page.evaluate("([t, c]) => edit(t, c)", ["homelines-tile", {"type": "custom:homelines-tile", "name": "Telefon"}])
    assert r["keys"] == ["name", "icon", "text", "warning", "error", "navigation_path", "entity"]
    out = page.evaluate("(v) => change(v)", {"text": "{{ states('sensor.telefon_status') }}", "icon": "mdi:phone"})
    assert out == {"type": "custom:homelines-tile", "name": "Telefon", "icon": "mdi:phone",
                   "text": "{{ states('sensor.telefon_status') }}"}


def test_stub_configs(page):
    stubs = page.evaluate("""() => ["homelines-card", "homelines-mini", "homelines-tile"]
        .map(t => [t, customElements.get(t).getStubConfig(), typeof customElements.get(t).getConfigElement])""")
    assert all(s[2] == "function" for s in stubs)
    assert dict((s[0], s[1]) for s in stubs)["homelines-mini"] == {"layout": "tile", "name": "Internet"}


async def test_central_line_names(hass, unifi, ping):
    """Namen aus den Optionen gelten für alle Karten (Snapshot) und stehen am Sensor der aktiven Leitung."""
    _, hub = await _setup(hass, options={**OPTIONS, "line_name_wan2": "DSL zu Hause", "line_name_wan1": "Glasfaser"})
    lines = {l["id"]: l for l in hub.snapshot()["wans"]}
    assert lines["WAN2"]["name"] == "DSL zu Hause"
    assert lines["WAN1"]["name"] == "Glasfaser"
    assert lines["WAN3"]["name"] == "5G Backup"  # ohne eigenen Namen: Name aus dem Router
    st = hass.states.get("sensor.homelines_active_wan")
    assert st.state == "WAN2" and st.attributes["name"] == "DSL zu Hause"


async def test_options_offer_line_names(hass, unifi, ping):
    entry, _ = await _setup(hass)
    r = await hass.config_entries.options.async_init(entry.entry_id)
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "lines"})
    keys = {str(k) for k in r["data_schema"].schema}
    assert {"line_name_wan1", "line_name_wan2", "line_name_wan3", "line_name_wan4"} <= keys
    strings = json.loads((CARD.parent.parent / "translations" / "de.json").read_text(encoding="utf-8"))
    assert strings["options"]["step"]["lines"]["data"]["line_name_wan2"] == "Name für WAN2"
