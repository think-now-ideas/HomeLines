"""0.9.0: Fenster-Baukasten in der Karte – eigene Fenster anzeigen, im Fenster bearbeiten und speichern,
Grafik-Optionen, Warnfarben, Euro mit zwei Nachkommastellen, Logo mit Schriftzug, FRITZ!Box-Vorlage.

Wie test_details_080: Karte in Chromium mit nachgebautem ``hass``, Daten aus einer echten HomeLines-Instanz.
"""
import json

import pytest
from homeassistant.helpers.json import JSONEncoder

from test_details_080 import CARD, PAGE
from test_homelines import _setup

STATES = {
    "sensor.speed_down": {"state": "231.4", "attributes": {"unit_of_measurement": "Mbit/s", "friendly_name": "Speedtest Download"}},
    "sensor.speed_up": {"state": "38.9", "attributes": {"unit_of_measurement": "Mbit/s", "friendly_name": "Speedtest Upload"}},
    "sensor.guthaben": {"state": "12.4", "attributes": {"unit_of_measurement": "€", "friendly_name": "Guthaben"}},
    "sensor.modem_dsl_snr": {"state": "5.2", "attributes": {"unit_of_measurement": "dB", "friendly_name": "DSL Rauschabstand"}},
    "sensor.fritz_box_rufnummer_1_status": {"state": "registered", "attributes": {"friendly_name": "Rufnummer 1"}},
    "sensor.fritz_box_rufnummer_2_status": {"state": "not registered", "attributes": {"friendly_name": "Rufnummer 2"}},
    "sensor.heizung_kueche_batterie": {"state": "15", "attributes": {"unit_of_measurement": "%", "device_class": "battery", "friendly_name": "Heizung Küche Batterie"}},
    "binary_sensor.drucker": {"state": "on", "attributes": {"device_class": "connectivity", "friendly_name": "Drucker"}},
    "sensor.fritz_box_cpu_temperatur": {"state": "58", "attributes": {"unit_of_measurement": "°C", "device_class": "temperature", "friendly_name": "FRITZ!Box CPU-Temperatur"}},
    "update.fritz_box_fritz_os": {"state": "off", "attributes": {"friendly_name": "FRITZ!OS"}},
}
REG = {
    "sensor.fritz_box_rufnummer_1_status": {"platform": "fritz"}, "sensor.fritz_box_rufnummer_2_status": {"platform": "fritz"},
    "sensor.heizung_kueche_batterie": {"platform": "fritzbox", "area_id": "kueche"},
    "binary_sensor.drucker": {"platform": "ping", "area_id": "buero"},
    "sensor.fritz_box_cpu_temperatur": {"platform": "fritz"}, "update.fritz_box_fritz_os": {"platform": "fritz"},
    "sensor.guthaben": {"platform": "template", "area_id": "buero"},
}
SPEED = [
    {"t": "values", "title": "Jetzt", "ents": ["sensor.speed_down", "sensor.guthaben", "sensor.gibt_es_nicht"],
     "rules": [{"c": "warn", "any": "any", "grp": "all", "when": "above", "v": "200"}], "style": "tiles"},
    {"t": "chart", "title": "Speedtests", "ents": ["sensor.speed_down", "sensor.speed_up"], "kind": "bar", "range": "7d",
     "mode": "together", "colors": {"sensor.speed_up": "orange"}, "limit": {"on": True, "v": "50", "dir": "below", "c": "err"}, "stats": True},
    {"t": "text", "text": "Speedtest läuft nachts.", "tone": "warn"},
    {"t": "chart", "title": "Fläche", "ents": ["sensor.modem_dsl_snr"], "kind": "area", "range": "24h",
     "mode": "separate", "colors": {}, "limit": {"on": False, "v": "", "dir": "below", "c": "warn"}, "stats": False},
]


async def _open(hass, unifi, ping, windows=None):
    _, hub = await _setup(hass)
    if windows:
        await hub.async_set_windows(windows)
    pw = pytest.importorskip("playwright.async_api")
    snap = json.dumps(hub.snapshot(), cls=JSONEncoder)
    p = await pw.async_playwright().start()
    browser = await p.chromium.launch()
    page = await browser.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    await page.set_content(PAGE.replace("%CARD%", CARD.read_text(encoding="utf-8")).replace("%SNAP%", snap))
    now = "Date.now()"
    await page.evaluate("""([st, reg]) => {
      Object.assign(HASS.states, st);
      const lat = (SNAP.details.own || {}).latency; if (lat) HASS.states[lat] = { state: '14.2', attributes: { unit_of_measurement: 'ms', friendly_name: 'Latenz' } }; HASS.entities = reg; HASS.user = { is_admin: true };
      HASS.areas = { kueche: { name: "Küche" }, buero: { name: "Arbeitszimmer" } }; HASS.devices = {};
      window.SENT = [];
      HASS.callWS = async (m) => {
        if (m.type === "homelines/set_windows") { SENT.push(m); const w = { ...(SNAP.windows || {}) };
          if (m.blocks) w[m.key] = m.blocks; else delete w[m.key]; SNAP.windows = w; return w; }
        if (m.type === "history/history_during_period") { const r = {}; const t = Date.now() / 1000;
          m.entity_ids.forEach(e => { r[e] = [0, 1, 2, 3, 4, 5, 6].map(k => ({ s: String(20 + 30 * k), lu: t - (7 - k) * 86400 })); }); return r; }
        return {}; };
    }""", [STATES, REG])
    await page.evaluate("add('homelines-card', {})")
    await page.wait_for_function("document.querySelector('homelines-card').shadowRoot.querySelector('.line')")
    return p, browser, page, errors


async def _detail(page, kind):
    await page.evaluate(f"document.querySelector('homelines-card')._openDetail('{kind}')")
    await page.wait_for_selector("homelines-detail .hld")
    await page.wait_for_timeout(150)


async def test_logo_with_wordmark(hass, unifi, ping):
    p, browser, page, errors = await _open(hass, unifi, ping)
    try:
        r = await page.evaluate("""() => { const sr = document.querySelector('homelines-card').shadowRoot;
          return { word: !!sr.querySelector('.hd svg.hlword'), house: !!sr.querySelector('.hd svg.hllogo'),
                   label: sr.querySelector('.hd svg.hlword') && sr.querySelector('.hd svg.hlword').getAttribute('aria-label'),
                   paths: sr.querySelectorAll('.hd svg.hlword g path').length }; }""")
        assert r == {"word": True, "house": False, "label": "HomeLines", "paths": 9}
        # eigener Titel: Haus + Titel
        await page.evaluate("document.body.innerHTML=''; add('homelines-card', { title: 'Internet' })")
        await page.wait_for_function("document.querySelector('homelines-card').shadowRoot.querySelector('.ttl')")
        t = await page.evaluate("document.querySelector('homelines-card').shadowRoot.querySelector('.ttl').textContent")
        assert t == "Internet"
        assert not errors, errors
    finally:
        await browser.close(); await p.stop()


async def test_custom_window_renders(hass, unifi, ping):
    p, browser, page, errors = await _open(hass, unifi, ping, {"speed": SPEED})
    try:
        await _detail(page, "speed")
        r = await page.evaluate("""() => { const d = document.querySelector('homelines-detail');
          return { custom: d._spec.custom, key: d._spec.key,
            vals: [...d.querySelectorAll('.hld-v')].map(v => [v.dataset.e, v.className.replace(/\\s+/g,' ').trim(), v.querySelector('.hld-x').textContent]),
            bars: d.querySelectorAll('.hld-c svg rect').length, limit: !!d.querySelector('.hld-c svg line[stroke-dasharray]'),
            stats: d.querySelector('.hld-stats') && d.querySelector('.hld-stats').textContent,
            hint: d.querySelector('.hld-hint.warn') && d.querySelector('.hld-hint.warn').textContent,
            tools: !!d.querySelector('[data-ed=start]'), area: !!d.querySelector('.hld-c path[opacity]') }; }""")
        assert r["custom"] is True and r["key"] == "speed" and r["tools"] is True and r["area"] is True
        assert r["vals"][0] == ["sensor.speed_down", "hld-v warn", "231 Mbit/s"]          # über 200 → gelb
        assert r["vals"][1][2] == "12,40 €"                                                # Euro: zwei Nachkommastellen
        assert r["vals"][2] == ["sensor.gibt_es_nicht", "hld-v na miss", "Wert fehlt"]
        assert r["bars"] > 20 and r["limit"] is True
        assert "Min" in r["stats"] and "Ø" in r["stats"]
        assert r["hint"] == "Speedtest läuft nachts."
        assert not errors, errors
    finally:
        await browser.close(); await p.stop()


async def test_edit_window_and_save(hass, unifi, ping):
    p, browser, page, errors = await _open(hass, unifi, ping)
    try:
        await _detail(page, "outages")
        assert await page.evaluate("document.querySelector('homelines-detail')._spec.custom") is False
        await page.click("homelines-detail [data-ed=start]")
        before = await page.evaluate("document.querySelectorAll('homelines-detail .hle-b').length")
        assert before >= 2   # eingebautes Fenster als Ausgangspunkt
        # Grafik einstellen: erster Grafik-Baustein → Fläche, 24 h, Grenzlinie
        idx = await page.evaluate("document.querySelector('homelines-detail')._edit.draft.findIndex(b => b.t === 'chart')")
        await page.click(f"homelines-detail [data-ed=sel][data-i='{idx}']")
        await page.click(f"homelines-detail [data-ed=setv][data-bi='{idx}'][data-f=kind][data-v=area]")
        await page.click(f"homelines-detail [data-ed=setv][data-bi='{idx}'][data-f=range][data-v='24h']")
        await page.click(f"homelines-detail [data-ed=flip][data-bi='{idx}'][data-f='limit.on']")
        await page.fill(f"homelines-detail input[data-f='limit.v'][data-i='{idx}']", "100")
        await page.dispatch_event(f"homelines-detail input[data-f='limit.v'][data-i='{idx}']", "change")
        # neuer Baustein: Hinweistext
        await page.click("homelines-detail [data-ed=addopen]")
        await page.click("homelines-detail [data-ed=add][data-v=text]")
        await page.fill("homelines-detail textarea[data-f=text]", "Nur zum Testen")
        await page.dispatch_event("homelines-detail textarea[data-f=text]", "change")
        # nach oben schieben
        n = await page.evaluate("document.querySelector('homelines-detail')._edit.draft.length")
        await page.click(f"homelines-detail [data-ed=up][data-i='{n - 1}']")
        await page.click("homelines-detail [data-ed=save]")
        await page.wait_for_function("SENT.length === 1 && !document.querySelector('homelines-detail')._edit")
        sent = await page.evaluate("SENT[0]")
        assert sent["key"] == "outages"
        chart = [b for b in sent["blocks"] if b["t"] == "chart"][0]
        assert chart["kind"] == "area" and chart["range"] == "24h" and chart["limit"] == {"on": True, "v": "100", "dir": "below", "c": "warn"}
        assert sent["blocks"][-2] == {"t": "text", "text": "Nur zum Testen", "tone": "info"}
        r = await page.evaluate("""() => { const d = document.querySelector('homelines-detail');
          return { custom: d._spec.custom, hint: [...d.querySelectorAll('.hld-hint')].map(x => x.textContent) }; }""")
        assert r["custom"] is True and "Nur zum Testen" in r["hint"]
        # zurück auf das eingebaute Fenster
        await page.click("homelines-detail [data-ed=start]")
        await page.click("homelines-detail [data-ed=reset]")
        await page.wait_for_function("SENT.length === 2")
        assert "blocks" not in await page.evaluate("SENT[1]")
        assert await page.evaluate("document.querySelector('homelines-detail')._spec.custom") is False
        assert not errors, errors
    finally:
        await browser.close(); await p.stop()


async def test_entity_picker_and_fritz_template(hass, unifi, ping):
    p, browser, page, errors = await _open(hass, unifi, ping, {"speed": SPEED})
    try:
        await _detail(page, "speed")
        await page.click("homelines-detail [data-ed=start]")
        await page.click("homelines-detail [data-ed=sel][data-i='0']")
        # fehlende Entität ersetzen
        assert await page.evaluate("document.querySelector('homelines-detail .hle-miss').textContent") == "1 Wert fehlt"
        await page.click("homelines-detail .hle-ent.miss [data-ed=pick]")
        await page.fill("homelines-detail [data-pq]", "upload")
        names = await page.evaluate("[...document.querySelectorAll('homelines-detail .hle-pi')].map(b => b.dataset.v)")
        assert names == ["sensor.speed_up"]
        await page.click("homelines-detail .hle-pi[data-v='sensor.speed_up']")
        ents = await page.evaluate("document.querySelector('homelines-detail')._edit.draft[0].ents")
        assert ents == ["sensor.speed_down", "sensor.guthaben", "sensor.speed_up"]
        # Bereich als Filter
        await page.click("homelines-detail [data-ed=pick][data-bi='0']:not([data-i])")
        await page.click("homelines-detail [data-ed=ptab][data-v=all]")
        await page.click("homelines-detail .hle-chips [data-v='Küche']")
        names = await page.evaluate("[...document.querySelectorAll('homelines-detail .hle-pi')].map(b => b.dataset.v)")
        assert names == ["sensor.heizung_kueche_batterie"]
        await page.click("homelines-detail .hle-dh [data-ed=pclose]")
        # FRITZ!Box-Vorlage: über die Integrationen gefunden
        await page.click("homelines-detail [data-ed=fritz]")
        d = await page.evaluate("document.querySelector('homelines-detail')._edit.draft.slice(4)")
        assert [b["title"] for b in d] == ["Telefonie", "Heizung (DECT)", "WLAN-Geräte", "Router", "CPU-Temperatur"]
        assert d[0]["ents"] == ["sensor.fritz_box_rufnummer_1_status", "sensor.fritz_box_rufnummer_2_status"]
        assert d[3]["ents"] == ["sensor.fritz_box_cpu_temperatur", "update.fritz_box_fritz_os"]
        dots = await page.evaluate("""() => [...document.querySelectorAll('homelines-detail .hle-b')].slice(4, 6)
          .map(b => [...b.querySelectorAll('.hld-row .dot')].map(x => x.className.replace('dot ', '')))""")
        assert dots == [["ok", "err"], ["warn"]]      # Rufnummer 2 nicht registriert, Batterie 15 %
        assert not errors, errors
    finally:
        await browser.close(); await p.stop()


async def test_not_admin_has_no_pen(hass, unifi, ping):
    p, browser, page, errors = await _open(hass, unifi, ping)
    try:
        await page.evaluate("HASS.user = { is_admin: false }")
        await page.evaluate("document.body.innerHTML=''; add('homelines-card', {})")
        await page.wait_for_function("document.querySelector('homelines-card').shadowRoot.querySelector('.line')")
        await _detail(page, "outages")
        assert await page.evaluate("!!document.querySelector('homelines-detail [data-ed=start]')") is False
        assert not errors, errors
    finally:
        await browser.close(); await p.stop()
