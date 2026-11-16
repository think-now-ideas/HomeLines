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


async def _open(hass, unifi, ping, windows=None, layout=None):
    _, hub = await _setup(hass)
    if windows:
        await hub.async_set_windows(windows)
    if layout:
        await hub.async_set_layout(layout)
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
        if (m.type === "homelines/set_layout") { SENT.push(m); if (m.layout) SNAP.layout = m.layout; return SNAP.layout; }
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


# ---------------------------------------------------------------------- 0.9.1: Karte direkt bearbeiten
CARD_SR = "document.querySelector('homelines-card').shadowRoot"


async def test_edit_card_layout(hass, unifi, ping):
    p, browser, page, errors = await _open(hass, unifi, ping)
    try:
        await page.evaluate("""() => { document.body.innerHTML = ''; add('homelines-card', { tiles: [
          { name: 'Strom', icon: 'mdi:flash', entities: ['sensor.speed_down', 'sensor.weg'], combine: 'sum', warn_unavailable: true, warn_above: 500 }] }); }""")
        await page.wait_for_function(f"{CARD_SR}.querySelector('.hlpen')")
        await page.evaluate(f"{CARD_SR}.querySelector('.hlpen').click()")
        r = await page.evaluate(f"""() => {{ const sr = {CARD_SR};
          return {{ pens: [...sr.querySelectorAll('.hlpn')].map(b => b.dataset.v), miss: sr.querySelector('.hlmiss') && sr.querySelector('.hlmiss').textContent,
            rows: sr.host._ed.layout.rows.map(r => r.id), rules: sr.host._ed.layout.rows.find(r => r.kind === 'tile').rules }}; }}""")
        assert "head" in r["pens"] and "line:WAN2" in r["pens"] and "row:t-strom" in r["pens"] and "row:outages" in r["pens"]
        assert r["miss"] == "1 Wert fehlt"
        assert r["rows"][-1] == "t-strom"
        assert r["rules"] == [{"c": "warn", "any": "any", "grp": "all", "when": "unavail", "v": ""},
                              {"c": "warn", "any": "any", "grp": "all", "when": "above", "v": "500"}]
        # Kachel wählen, umbenennen, nach oben, fehlende Entität ersetzen
        await page.evaluate(f"{CARD_SR}.querySelector('[data-v=\"row:t-strom\"]').click()")
        await page.evaluate(f"""() => {{ const i = {CARD_SR}.querySelector('[data-cf=rname]'); i.value = 'Leistung'; i.dispatchEvent(new Event('change', {{ bubbles: true, composed: true }})); }}""")
        await page.evaluate(f"{CARD_SR}.querySelector('[data-ce=up]').click()")
        await page.evaluate(f"{CARD_SR}.querySelector('.hlent.miss [data-ce=pick]').click()")
        await page.wait_for_selector(".hlpk input")
        await page.fill(".hlpk input", "upload")
        await page.click(".hlpk .it[data-v='sensor.speed_up']")
        await page.wait_for_function(f"!{CARD_SR}.querySelector('.hlent.miss')")
        # Geschwindigkeit ausblenden, Leitung umbenennen, Titel
        await page.evaluate(f"{CARD_SR}.querySelector('[data-v=\"row:outages\"]').click()")
        await page.evaluate(f"{CARD_SR}.querySelector('[data-ce=flip]').click()")
        await page.evaluate(f"{CARD_SR}.querySelector('[data-v=\"line:WAN2\"]').click()")
        await page.evaluate(f"""() => {{ const i = {CARD_SR}.querySelector('[data-cf="name:WAN2"]'); i.value = 'Kupfer'; i.dispatchEvent(new Event('change', {{ bubbles: true, composed: true }})); }}""")
        # Assistent: neue Kachel „Batterien“
        await page.evaluate(f"{CARD_SR}.querySelector('.hladd').click()")
        await page.click(".hlpk [data-k=battery]")
        await page.click(".hlpk [data-make]")
        await page.wait_for_function(f"{CARD_SR}.host._ed.layout.rows.some(r => r.name === 'Batterien')")
        await page.evaluate(f"{CARD_SR}.querySelector('[data-ce=save]').click()")
        await page.wait_for_function("SENT.filter(m => m.type === 'homelines/set_layout').length === 1")
        sent = await page.evaluate("SENT")
        lay = [m for m in sent if m["type"] == "homelines/set_layout"][0]
        win = [m for m in sent if m["type"] == "homelines/set_windows"]
        rows = lay["layout"]["rows"]
        tile = [r for r in rows if r["id"] == "t-strom"][0]
        assert tile["name"] == "Leistung" and tile["entities"] == ["sensor.speed_down", "sensor.speed_up"]
        assert [r["id"] for r in rows].index("t-strom") < [r["id"] for r in rows].index("outages")
        assert [r for r in rows if r["id"] == "outages"][0]["on"] is False
        bat = [r for r in rows if r.get("name") == "Batterien"][0]
        assert bat["entities"] == ["sensor.heizung_kueche_batterie"] and bat["combine"] == "min"
        assert lay["line_names"] == {"WAN2": "Kupfer"}
        assert win and win[0]["key"] == bat["id"] and win[0]["blocks"][0]["t"] == "values"
        # nach dem Speichern: Aufbau aus HomeLines, Geschwindigkeit weg, Kachel mit neuem Namen
        await page.wait_for_function(f"!{CARD_SR}.host._ed")
        r = await page.evaluate(f"""() => {{ const sr = {CARD_SR};
          return {{ speed: !!sr.querySelector('[data-ok=outages]'), tiles: [...sr.querySelectorAll('homelines-tile')].map(t => t._c.name), pen: !!sr.querySelector('.hlpen') }}; }}""")
        assert r == {"speed": False, "tiles": ["Leistung", "Batterien"], "pen": True}
        assert not errors, errors
    finally:
        await browser.close(); await p.stop()


async def test_layout_tile_rules_and_no_pen_for_users(hass, unifi, ping):
    lay = {"title": "Netz", "hide_lines": ["WAN3"], "rows": [
        {"id": "t-akku", "kind": "tile", "on": True, "name": "Akku", "icon": "mdi:battery-60",
         "entities": ["sensor.heizung_kueche_batterie"], "combine": "min",
         "rules": [{"c": "err", "any": "any", "grp": "all", "when": "below", "v": "20"}], "second": "none"},
        {"id": "outages", "kind": "builtin", "on": True}]}
    p, browser, page, errors = await _open(hass, unifi, ping, layout=lay)
    try:
        await page.evaluate("document.body.innerHTML=''; HASS.user = { is_admin: false }; add('homelines-card', {})")
        await page.wait_for_function(f"{CARD_SR}.querySelector('homelines-tile')")
        await page.wait_for_timeout(100)
        r = await page.evaluate(f"""() => {{ const sr = {CARD_SR}, t = sr.querySelector('homelines-tile');
          return {{ title: sr.querySelector('.ttl') && sr.querySelector('.ttl').textContent, wan3: !!sr.querySelector('[data-wid=WAN3]'),
            err: t.shadowRoot.querySelector('ha-card').className, pen: !!sr.querySelector('.hlpen'),
            order: [...sr.querySelectorAll('[data-ok]')].map(x => x.dataset.ok) }}; }}""")
        assert r["title"] == "Netz" and r["wan3"] is False and r["pen"] is False
        assert "err" in r["err"]
        assert r["order"][0] == "x0" and "outages" in r["order"]
        assert not errors, errors
    finally:
        await browser.close(); await p.stop()


# ---------------------------------------------------------------------- 0.9.2: melden, sichern und laden
async def test_notify_and_backup_restore(hass, unifi, ping, tmp_path):
    lay = {"title": "", "hide_lines": [], "rows": [
        {"id": "t-akku", "kind": "tile", "on": True, "name": "Akku", "icon": "mdi:battery-60",
         "entities": ["sensor.heizung_kueche_batterie"], "combine": "min",
         "rules": [{"c": "warn", "any": "any", "grp": "all", "when": "below", "v": "20"}], "second": "none"}]}
    p, browser, page, errors = await _open(hass, unifi, ping, {"speed": SPEED}, layout=lay)
    try:
        await page.evaluate("document.body.innerHTML=''; add('homelines-card', {})")
        await page.wait_for_function(f"{CARD_SR}.querySelector('.hlpen')")
        await page.evaluate(f"{CARD_SR}.querySelector('.hlpen').click()")
        # Text zum Markieren enthält Aufbau und Fenster
        await page.evaluate(f"{CARD_SR}.querySelector('[data-ce=showjson]').click()")
        txt = await page.evaluate(f"{CARD_SR}.querySelector('textarea').value")
        import json as _j
        backup = _j.loads(txt)
        assert backup["layout"]["rows"][0]["id"] == "t-akku" and "speed" in backup["windows"]
        # Warnfarbe melden
        await page.evaluate(f"{CARD_SR}.querySelector('[data-v=\"row:t-akku\"]').click()")
        await page.evaluate(f"""() => {{ const i = {CARD_SR}.querySelector('[data-cf="rule:0:notify"]'); i.value = '1'; i.dispatchEvent(new Event('change', {{ bubbles: true, composed: true }})); }}""")
        assert "Konfigurieren → Meldungen" in await page.evaluate(f"{CARD_SR}.querySelector('.hlpanel').textContent")
        await page.evaluate(f"{CARD_SR}.querySelector('[data-ce=save]').click()")
        await page.wait_for_function("SENT.some(m => m.type === 'homelines/set_layout')")
        sent = await page.evaluate("SENT.find(m => m.type === 'homelines/set_layout')")
        assert sent["layout"]["rows"][0]["rules"][0]["notify"] is True
        # Laden: Datei mit anderem Aufbau und Fenster
        backup["layout"]["rows"][0]["name"] = "Batterien"
        backup["windows"] = {"outages": [{"t": "text", "text": "geladen", "tone": "info"}]}
        f = tmp_path / "homelines-einstellungen.json"
        f.write_text(_j.dumps(backup), encoding="utf-8")
        await page.wait_for_function(f"!{CARD_SR}.host._ed")
        await page.evaluate(f"{CARD_SR}.querySelector('.hlpen').click()")
        await page.evaluate("SENT.length = 0")
        await page.set_input_files("homelines-card >> input[data-cf=import]", str(f))
        await page.wait_for_function(f"{CARD_SR}.querySelector('[data-ce=loadok]')")
        await page.evaluate(f"{CARD_SR}.querySelector('[data-ce=loadok]').click()")
        await page.wait_for_function("SENT.length === 2")
        s = await page.evaluate("SENT")
        assert s[0]["type"] == "homelines/set_windows" and s[0]["windows"] == backup["windows"]
        assert s[1]["layout"]["rows"][0]["name"] == "Batterien"
        assert not errors, errors
    finally:
        await browser.close(); await p.stop()
