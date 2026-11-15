"""0.8.0: Detailansichten aus den Optionen, eingebaute Detailfenster der Karte, Mini-Karte ohne eigene Sensoren.

Die Karte läuft in Chromium (Playwright) mit nachgebautem ``hass``; die Daten kommen aus einer echten
HomeLines-Instanz (``hub.snapshot()``). ``loadCardHelpers`` liefert Platzhalter, die ihre Konfiguration zeigen.
"""
import json
from pathlib import Path

import pytest
from homeassistant.helpers.json import JSONEncoder

from test_homelines import BASE, OPTIONS, _setup

CARD = Path(__file__).parent.parent / "custom_components" / "homelines" / "www" / "homelines-card.js"

DETAILS = {
    **OPTIONS,
    "details_wan2": ["sensor.modem_dsl_sync", "sensor.modem_dsl_snr"],
    "history_wan2": ["sensor.modem_dsl_sync"],
    "speed_download": "sensor.speed_down", "speed_upload": "sensor.speed_up",
    "backup_extra": ["sensor.notfall_router_leistung"],
    "line_name_wan2": "DSL",
}

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script>
customElements.define("ha-icon", class extends HTMLElement {});
customElements.define("ha-card", class extends HTMLElement {});
window.loadCardHelpers = async () => ({ createCardElement: (cfg) => {
  const el = document.createElement("div"); el.className = "stub"; el.dataset.cfg = JSON.stringify(cfg); return el; } });
</script>
<script>%CARD%</script></head><body>
<script>
window.SNAP = %SNAP%;
window.HIST = [];
window.HASS = {
  states: { "sensor.speed_down": { state: "231.4", attributes: { unit_of_measurement: "Mbit/s" } },
            "sensor.speed_up": { state: "38.9", attributes: { unit_of_measurement: "Mbit/s" } } },
  callWS: async (m) => { HIST.push(m.entity_ids); return {}; }, callService: async () => {},
  connection: {
    addEventListener() {}, removeEventListener() {},
    subscribeMessage: async (cb, msg) => { if (msg.type === "homelines/subscribe") setTimeout(() => cb(SNAP), 0); return () => {}; },
    sendMessagePromise: async () => ({}) } };
window.add = (type, cfg) => { const el = document.createElement(type); el.setConfig(cfg); document.body.appendChild(el); el.hass = HASS; return el; };
window.pops = () => [...document.querySelectorAll("body > .hl-pop")].map(p => ({
  title: (p.querySelector(".pt") || {}).textContent || null, shown: p.style.display !== "none",
  cards: [...p.querySelectorAll(".stub")].map(s => JSON.parse(s.dataset.cfg)) }));
</script></body></html>"""


async def _page(hass, hub):
    pw = pytest.importorskip("playwright.async_api")
    snap = json.dumps(hub.snapshot(), cls=JSONEncoder)
    p = await pw.async_playwright().start()
    browser = await p.chromium.launch()
    page = await browser.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    await page.set_content(PAGE.replace("%CARD%", CARD.read_text(encoding="utf-8")).replace("%SNAP%", snap))
    return p, browser, page, errors


async def test_snapshot_details(hass, unifi, ping):
    _, hub = await _setup(hass, options=DETAILS)
    d = hub.snapshot()["details"]
    assert d["lines"] == {"WAN2": {"entities": ["sensor.modem_dsl_sync", "sensor.modem_dsl_snr"],
                                   "history": ["sensor.modem_dsl_sync"]}}
    assert d["speed"] == {"download": "sensor.speed_down", "upload": "sensor.speed_up"}
    assert d["backup"] == ["sensor.notfall_router_leistung"]
    assert d["own"]["status"] == "sensor.homelines_status" and d["own"]["test_notify"] == "button.homelines_test_notify"
    assert "sensor.notfall_handy_battery" in d["phone"]
    lines = {w["id"]: w for w in hub.snapshot()["wans"]}
    assert lines["WAN2"]["primary"] is True and lines["WAN3"]["primary"] is False


async def test_options_details_step(hass, unifi, ping):
    entry, _ = await _setup(hass)
    r = await hass.config_entries.options.async_init(entry.entry_id)
    assert "details" in r["menu_options"]
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"next_step_id": "details"})
    keys = {str(k) for k in r["data_schema"].schema}
    assert {"details_wan1", "history_wan4", "speed_download", "speed_upload", "backup_extra"} <= keys
    r = await hass.config_entries.options.async_configure(r["flow_id"], {
        "details_wan2": ["sensor.modem_dsl_sync"], "speed_download": "sensor.speed_down"})
    assert entry.options["details_wan2"] == ["sensor.modem_dsl_sync"]
    assert entry.options["speed_download"] == "sensor.speed_down"


async def test_card_detail_windows(hass, unifi, ping):
    data = {**BASE, "reconnect_enabled": True, "ssh_host": "192.168.1.1", "ssh_port": 22, "ssh_user": "root",
            "ssh_password": "pw", "ppp_interface": "ppp1", "reconnect_method": "pppd_hup", "reconnect_time": "04:00:00"}
    _, hub = await _setup_with_data(hass, data, DETAILS)
    p, browser, page, errors = await _page(hass, hub)
    try:
        await page.evaluate("add('homelines-card', { compact: true })")
        await page.wait_for_function("document.querySelector('homelines-card').shadowRoot.querySelector('.line')")
        root = "document.querySelector('homelines-card').shadowRoot"
        # Geschwindigkeit als Chip, Name aus den Optionen
        txt = await page.evaluate(f"{root}.getElementById('main').innerText")
        assert "↓ 231 · ↑ 39 Mbit/s" in txt and "DSL" in txt

        # Hauptleitung: Werte, Verlauf, Neueinwahl
        await page.evaluate(f"{root}.querySelector('.line[data-id=WAN2]').click()")
        await page.wait_for_function("document.querySelectorAll('.hl-pop .stub').length >= 4")
        w2 = (await page.evaluate("pops()"))[-1]
        assert w2["title"] == "DSL (WAN2)"
        types = [c["type"] for c in w2["cards"]]
        assert types[:3] == ["tile", "tile", "tile"] and "history-graph" in types and "entities" in types
        assert {"entity": "sensor.modem_dsl_snr", "type": "tile"} in w2["cards"]
        rec = next(c for c in w2["cards"] if c["type"] == "entities")
        assert "button.homelines_reconnect_now" in rec["entities"] and "switch.homelines_daily_reconnect" in rec["entities"]
        await page.evaluate("history.back()")
        await page.wait_for_function("!document.querySelector('.hl-pop')")

        # Backup-Leitung: Notfall-Strecke mit HomeLines-Werten, Handy und weiteren Werten
        await page.evaluate(f"{root}.querySelector('.line[data-id=WAN3]').click()")
        await page.wait_for_function("document.querySelectorAll('.hl-pop .stub').length > 5")
        ents = [c.get("entity") for c in (await page.evaluate("pops()"))[-1]["cards"]]
        assert {"sensor.homelines_status", "binary_sensor.homelines_phone", "sensor.homelines_cost",
                "sensor.notfall_handy_battery", "sensor.notfall_router_leistung"} <= set(ents)
        assert not any(c.get("type") == "entities" for c in (await page.evaluate("pops()"))[-1]["cards"])
        await page.evaluate("history.back()")
        await page.wait_for_function("!document.querySelector('.hl-pop')")

        # Kennzahlen → Ausfälle, Geschwindigkeit
        await page.evaluate(f"{root}.querySelector('[data-k=outages]').click()")
        await page.wait_for_function("document.querySelectorAll('.hl-pop .stub').length > 0")
        out = (await page.evaluate("pops()"))[-1]
        assert out["title"] == "Ausfälle und Verlauf"
        assert {"type": "tile", "entity": "sensor.homelines_availability_7d"} in out["cards"]
        await page.evaluate("history.back()")
        await page.evaluate(f"{root}.querySelector('[data-k=speed]').click()")
        await page.wait_for_function("document.querySelectorAll('.hl-pop .stub').length > 0")
        sp = (await page.evaluate("pops()"))[-1]
        assert sp["title"] == "Geschwindigkeit"
        assert sp["cards"][-1] == {"type": "history-graph", "title": "Verlauf", "hours_to_show": 168,
                                   "entities": ["sensor.speed_down", "sensor.speed_up"]}
        assert not errors, errors
    finally:
        await browser.close()
        await p.stop()


async def test_mini_uses_option_sensors_and_stacked_windows(hass, unifi, ping):
    _, hub = await _setup(hass, options=DETAILS)
    p, browser, page, errors = await _page(hass, hub)
    try:
        await page.evaluate("add('homelines-mini', { layout: 'bar' })")
        await page.wait_for_function("document.querySelector('homelines-mini').shadowRoot.querySelector('.s')")
        await page.wait_for_function("HIST.length > 0")
        assert (await page.evaluate("HIST"))[-1] == ["sensor.speed_down", "sensor.speed_up"]
        txt = await page.evaluate("document.querySelector('homelines-mini').shadowRoot.querySelector('.s').innerText")
        assert "↓ 231 · ↑ 39 Mbit/s" in txt

        # Mini → große Karte im Fenster → Leitung → zweites Fenster; Zurück schließt nur das obere
        await page.evaluate("document.querySelector('homelines-mini').shadowRoot.querySelector('ha-card').click()")
        await page.wait_for_function("document.querySelector('.hl-pop homelines-card')?.shadowRoot?.querySelector('.line')")
        await page.evaluate("document.querySelector('.hl-pop homelines-card').shadowRoot.querySelector('.line[data-id=WAN2]').click()")
        await page.wait_for_function("document.querySelectorAll('body > .hl-pop').length === 2")
        await page.evaluate("history.back()")
        await page.wait_for_function("document.querySelectorAll('body > .hl-pop').length === 1")
        assert (await page.evaluate("pops()"))[0]["shown"] is True
        await page.keyboard.press("Escape")
        await page.wait_for_function("!document.querySelector('.hl-pop')")
        assert not errors, errors
    finally:
        await browser.close()
        await p.stop()


async def _setup_with_data(hass, data, options):
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    from custom_components.homelines.const import DOMAIN
    import test_homelines

    entry = MockConfigEntry(domain=DOMAIN, title="HomeLines", data=data, options=options)
    orig = test_homelines.MockConfigEntry
    test_homelines.MockConfigEntry = lambda **kw: entry
    try:
        return await _setup(hass, options=options)
    finally:
        test_homelines.MockConfigEntry = orig
