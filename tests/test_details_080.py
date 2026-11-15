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
    "speed_extra": ["button.speedtest_starten"],
    "backup_extra": ["sensor.notfall_router_leistung"],
    "monitor_extra": ["sensor.router_latenz"],
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
  states: { "sensor.modem_dsl_sync": { state: "62.4", attributes: { unit_of_measurement: "Mbit/s", friendly_name: "DSL Sync" } },
            "sensor.speed_down": { state: "231.4", attributes: { unit_of_measurement: "Mbit/s" } },
            "sensor.speed_up": { state: "38.9", attributes: { unit_of_measurement: "Mbit/s" } } },
  callWS: async (m) => { HIST.push(m.entity_ids); return {}; }, callService: async () => {},
  connection: {
    addEventListener() {}, removeEventListener() {},
    subscribeMessage: async (cb, msg) => { if (msg.type === "homelines/subscribe") setTimeout(() => cb(SNAP), 0); return () => {}; },
    sendMessagePromise: async () => ({}) } };
window.add = (type, cfg) => { const el = document.createElement(type); el.setConfig(cfg); document.body.appendChild(el); el.hass = HASS; return el; };
window.pops = () => [...document.querySelectorAll("body > .hl-pop")].map(p => {
  const d = p.querySelector("homelines-detail"), bl = ((d && d._spec) || {}).blocks || [];
  const of = t => bl.filter(b => b.type === t).flatMap(b => b.entities || []);
  return { title: (p.querySelector(".pt") || {}).textContent || null, shown: p.style.display !== "none",
    values: of("values"), charts: of("chart"), controls: of("controls"), timelines: of("timeline"), types: bl.map(b => b.type),
    shownValues: d ? [...d.querySelectorAll(".hld-v")].map(v => [v.dataset.e, v.querySelector(".hld-x").textContent]) : [],
    cards: [...p.querySelectorAll(".stub")].map(s => JSON.parse(s.dataset.cfg)) }; });
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
    assert d["speed"] == {"download": "sensor.speed_down", "upload": "sensor.speed_up",
                          "extra": ["button.speedtest_starten"]}
    assert d["backup"] == ["sensor.notfall_router_leistung"]
    assert d["monitor"] == ["sensor.router_latenz"]
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
    assert {"details_wan1", "history_wan4", "speed_download", "speed_upload", "speed_extra", "backup_extra"} <= keys
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

        # Hauptleitung: Werte, Verlauf, Neueinwahl – von HomeLines selbst gezeichnet
        await page.evaluate(f"{root}.querySelector('.line[data-id=WAN2]').click()")
        await page.wait_for_function("document.querySelector('.hl-pop homelines-detail .hld-v')")
        w2 = (await page.evaluate("pops()"))[-1]
        assert w2["title"] == "DSL (WAN2)"
        assert w2["values"][1:] == ["sensor.modem_dsl_sync", "sensor.modem_dsl_snr"]
        assert ["sensor.modem_dsl_sync", "62,4 Mbit/s"] in w2["shownValues"]
        assert w2["charts"] == ["sensor.modem_dsl_sync"]
        assert "button.homelines_reconnect_now" in w2["controls"] and "switch.homelines_daily_reconnect" in w2["controls"]
        assert w2["cards"][0]["type"] == "entities" and len(w2["cards"][0]["entities"]) == len(w2["controls"])
        await page.wait_for_function("HIST.some(h => h && h.includes('sensor.modem_dsl_sync'))")
        await page.evaluate("history.back()")
        await page.wait_for_function("!document.querySelector('.hl-pop')")

        # Backup-Leitung: Notfall-Strecke mit HomeLines-Werten, Handy und weiteren Werten
        await page.evaluate(f"{root}.querySelector('.line[data-id=WAN3]').click()")
        await page.wait_for_function("document.querySelector('.hl-pop homelines-detail')")
        w3 = (await page.evaluate("pops()"))[-1]
        assert {"sensor.homelines_status", "sensor.homelines_cost", "sensor.notfall_router_leistung"} <= set(w3["values"])
        assert w3["types"][0] == "phone" and "button.homelines_test_notify" in w3["controls"]
        assert w3["timelines"] == ["sensor.homelines_status"]
        await page.evaluate("history.back()")
        await page.wait_for_function("!document.querySelector('.hl-pop')")

        # Übersicht in der Karte: Zeilen öffnen dieselben Fenster
        rows = await page.evaluate(f"[...{root}.querySelectorAll('.hlov')].map(r => [r.dataset.k, r.innerText.replace(/\\s+/g, ' ').trim()])")
        assert [r[0] for r in rows] == ["line", "line", "speed", "outages"]
        assert rows[0][1].startswith("Notfall-Strecke")
        assert rows[1][1].startswith("DSL 62,4 Mbit/s")
        assert "↓ 231 Mbit/s · ↑ 39 Mbit/s" in rows[2][1]

        # Kennzahlen → Ausfälle, Geschwindigkeit
        await page.evaluate(f"{root}.querySelector('.chip[data-k=outages]').click()")
        await page.wait_for_function("document.querySelector('.hl-pop homelines-detail')")
        out = (await page.evaluate("pops()"))[-1]
        assert out["title"] == "Ausfälle und Verlauf"
        assert "sensor.homelines_availability_7d" in out["values"] and "binary_sensor.homelines_internet" in out["timelines"]
        assert "log" in out["types"] and "sensor.homelines_latency" in out["charts"]
        await page.evaluate("history.back()")
        await page.wait_for_function("!document.querySelector('.hl-pop')")
        await page.evaluate(f"{root}.querySelector('.chip[data-k=speed]').click()")
        await page.wait_for_function("document.querySelector('.hl-pop homelines-detail')")
        sp = (await page.evaluate("pops()"))[-1]
        assert sp["title"] == "Geschwindigkeit"
        assert sp["controls"] == ["button.speedtest_starten"] and sp["charts"] == ["sensor.speed_down", "sensor.speed_up"]
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


async def test_set_details_action(hass, unifi, ping):
    """0.8.3: alles in einem Rutsch per Aktion, danach wie im Formular gespeichert."""
    entry, _ = await _setup(hass, options={**OPTIONS, "details_wan1": ["sensor.alt"], "line_name_wan4": "Alt"})
    await hass.services.async_call("homelines", "set_details", {
        "line_names": {"WAN1": "Glasfaser", "wan2": "DSL"},
        "lines": {"WAN2": {"values": ["sensor.modem_dsl_sync", "sensor.modem_dsl_snr"], "history": ["sensor.modem_dsl_sync"]}},
        "speed_download": "sensor.speed_down", "speed_upload": "sensor.speed_up",
        "speed_extra": ["button.speedtest_starten"], "backup_extra": ["sensor.notfall_router_leistung"],
        "monitor_extra": ["sensor.router_latenz"],
    }, blocking=True)
    await hass.async_block_till_done()
    o = entry.options
    assert o["line_name_wan1"] == "Glasfaser" and o["line_name_wan2"] == "DSL" and o["line_name_wan4"] == "Alt"
    assert o["details_wan2"] == ["sensor.modem_dsl_sync", "sensor.modem_dsl_snr"] and o["history_wan2"] == ["sensor.modem_dsl_sync"]
    assert o["details_wan1"] == ["sensor.alt"]  # ohne replace bleibt Vorhandenes
    assert o["speed_extra"] == ["button.speedtest_starten"] and o["phone_rx"] == OPTIONS["phone_rx"]
    assert o["monitor_extra"] == ["sensor.router_latenz"]
    hub = hass.data["homelines"][entry.entry_id]  # nach dem Neuladen
    assert {w["id"]: w["name"] for w in hub.snapshot()["wans"]}["WAN2"] == "DSL"

    await hass.services.async_call("homelines", "set_details", {"replace": True, "speed_download": "sensor.speed_down"},
                                   blocking=True)
    await hass.async_block_till_done()
    o = entry.options
    assert "details_wan1" not in o and "line_name_wan4" not in o and o["speed_download"] == "sensor.speed_down"
    assert o["phone_rx"] == OPTIONS["phone_rx"]  # andere Optionen unberührt

    import pytest as _pt
    import voluptuous as _vol
    with _pt.raises(_vol.Invalid):
        await hass.services.async_call("homelines", "set_details", {"line_names": {"WAN7": "x"}}, blocking=True)


async def test_tile_without_templates(hass, unifi, ping):
    """0.8.4: Kachel aus Entitäten – Summe, Warnfarben per Formular, Tipp öffnet Fenster mit Werten und Verlauf."""
    _, hub = await _setup(hass, options=DETAILS)
    p, browser, page, errors = await _page(hass, hub)
    try:
        await page.evaluate("""Object.assign(HASS.states, {
          "sensor.p1": { state: "12.5", attributes: { unit_of_measurement: "W", friendly_name: "Router" } },
          "sensor.p2": { state: "20.6", attributes: { unit_of_measurement: "W", friendly_name: "Modem" } },
          "sensor.p3": { state: "unavailable", attributes: { unit_of_measurement: "W", friendly_name: "Notfall-Router" } } })""")
        await page.evaluate("""add('homelines-tile', { name: 'Strom', entities: ['sensor.p1', 'sensor.p2'], warn_above: 40, hours: 24 })""")
        tile = "document.querySelector('homelines-tile').shadowRoot"
        await page.wait_for_function(f"{tile}.querySelector('.s').textContent.length > 0")
        assert await page.evaluate(f"{tile}.querySelector('.s').textContent") == "33,1 W gesamt"
        assert await page.evaluate(f"{tile}.querySelector('ha-card').className") == ""

        # dritte Entität nicht erreichbar → gelb mit Hinweis; über 40 W → gelb
        await page.evaluate("""(() => { const t = document.querySelector('homelines-tile');
          t.setConfig({ name: 'Strom', entities: ['sensor.p1', 'sensor.p2', 'sensor.p3'], warn_unavailable: true }); t.hass = { ...HASS }; })()""")
        assert await page.evaluate(f"{tile}.querySelector('.s').textContent") == "33,1 W gesamt · 1 nicht erreichbar"
        assert await page.evaluate(f"{tile}.querySelector('ha-card').className") == "warn"
        await page.evaluate("""(() => { const t = document.querySelector('homelines-tile');
          t.setConfig({ name: 'Strom', entities: ['sensor.p1', 'sensor.p2'], error_above: 30 }); t.hass = { ...HASS }; })()""")
        assert await page.evaluate(f"{tile}.querySelector('ha-card').className") == "err"

        await page.evaluate(f"{tile}.querySelector('ha-card').click()")
        await page.wait_for_function("document.querySelector('.hl-pop homelines-detail .hld-v')")
        w = (await page.evaluate("pops()"))[-1]
        assert w["title"] == "Strom" and w["values"] == ["sensor.p1", "sensor.p2"] and w["charts"] == ["sensor.p1", "sensor.p2"]
        assert ["sensor.p1", "12,5 W"] in w["shownValues"]
        assert not errors, errors
    finally:
        await browser.close()
        await p.stop()


async def test_card_tiles_in_overview(hass, unifi, ping):
    """0.8.6: eigene Kacheln im Raster der Übersicht, zwei Spalten, kurze Namen."""
    _, hub = await _setup(hass, options=DETAILS)
    p, browser, page, errors = await _page(hass, hub)
    try:
        await page.evaluate("""Object.assign(HASS.states, {
          "sensor.p1": { state: "12.5", attributes: { unit_of_measurement: "W", friendly_name: "Router" } },
          "sensor.p2": { state: "20.6", attributes: { unit_of_measurement: "W", friendly_name: "Modem" } } })""")
        await page.evaluate("""add('homelines-card', { compact: true, tiles: [
          { name: 'Strom', icon: 'mdi:lightning-bolt', entities: ['sensor.p1', 'sensor.p2'] },
          { name: 'Telefon', entities: ['sensor.p1'], combine: 'single' }] })""")
        root = "document.querySelector('homelines-card').shadowRoot"
        await page.wait_for_function(f"{root}.querySelectorAll('.hlovx homelines-tile').length === 2")
        t0 = f"{root}.querySelectorAll('.hlovx homelines-tile')[0].shadowRoot"
        assert await page.evaluate(f"{t0}.querySelector('.s').textContent") == "33,1 W gesamt"
        assert "emb" in await page.evaluate(f"{t0}.querySelector('ha-card').className")
        cols = await page.evaluate(f"getComputedStyle({root}.querySelector('.hlovw')).gridTemplateColumns.split(' ').length")
        assert cols == 2
        # neu zeichnen behält die Kacheln
        await page.evaluate("(() => { const c = document.querySelector('homelines-card'); c._render(); })()")
        assert await page.evaluate(f"{root}.querySelectorAll('.hlovx homelines-tile').length") == 2
        await page.evaluate(f"{t0}.querySelector('ha-card').click()")
        await page.wait_for_function("document.querySelector('.hl-pop homelines-detail .hld-v')")
        names = await page.evaluate("hlCleanName('Router WAN (Leitung A / default) Router WAN Status')")
        assert names == "Router WAN Status"
        assert await page.evaluate("hlCleanName('Thermostat (DECT)')") == "Thermostat (DECT)"
        assert not errors, errors
    finally:
        await browser.close()
        await p.stop()


async def test_overview_hide_rows(hass, unifi, ping):
    """0.8.6: Übersichtszeilen einzeln ausblenden."""
    _, hub = await _setup(hass, options=DETAILS)
    p, browser, page, errors = await _page(hass, hub)
    try:
        await page.evaluate("add('homelines-card', { compact: true, overview_hide: { speed: true, outages: true } })")
        root = "document.querySelector('homelines-card').shadowRoot"
        await page.wait_for_function(f"{root}.querySelector('.hlov')")
        ks = await page.evaluate(f"[...{root}.querySelectorAll('.hlov')].map(r => r.dataset.k)")
        assert "speed" not in ks and "outages" not in ks and "line" in ks
        assert not errors, errors
    finally:
        await browser.close()
        await p.stop()


async def test_tiles_without_overview(hass, unifi, ping):
    """0.8.6: Übersicht aus – eigene Kacheln bleiben sichtbar."""
    _, hub = await _setup(hass, options=DETAILS)
    p, browser, page, errors = await _page(hass, hub)
    try:
        await page.evaluate("add('homelines-card', { compact: true, overview: false, tiles: [{ name: 'Telefon', text: 'ok' }] })")
        root = "document.querySelector('homelines-card').shadowRoot"
        await page.wait_for_function(f"{root}.querySelector('.hlovx homelines-tile')")
        assert await page.evaluate(f"{root}.querySelectorAll('.hlov').length") == 0
        assert not errors, errors
    finally:
        await browser.close()
        await p.stop()
