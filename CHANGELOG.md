# Änderungen

## 0.8.1 – Mehr Werte im Fenster „Geschwindigkeit“
- Neu in *Detailansichten der Karte*: „Geschwindigkeit: weitere Werte“, z. B. Ping und letzter Lauf des Speedtests,
  Knopf „Speedtest starten“ oder der Schalter für den automatischen Speedtest.
- Bei „Werte“ je Leitung und bei den weiteren Werten der Notfall-Strecke lassen sich jetzt auch Schalter und Buttons
  wählen (vorher nur Sensoren).

## 0.8.0 – Detailansichten eingebaut: eine Karte statt eigener Dashboard-Seite
- **Neu in den Optionen: „Detailansichten der Karte“.** Je Leitung (WAN1–WAN4) wählst du Sensoren für Werte (Kacheln)
  und Verlauf (Diagramm, 7 Tage), dazu die Sensoren für Download- und Upload-Geschwindigkeit und weitere Werte der
  Notfall-Strecke (z. B. Stromverbrauch des Notfall-Routers). Alles per Auswahlliste, kein YAML.
- **Eingebaute Detailfenster in der großen Karte:** Ein Tipp auf eine Leitung öffnet ein Fenster mit ihren Werten und
  dem Verlauf. Bei der Hauptleitung steht dort auch die Neueinwahl (Schalter, Uhrzeit, letzte Neueinwahl, Ergebnis,
  WAN-IP, „Jetzt neu verbinden“), bei der Backup-Leitung die Notfall-Strecke (Status, Handy meldet sich, Geräte online,
  Verbrauch, Kosten, Guthaben, Akku/Signal/Netz des Handys). Die Kennzahlen öffnen „Ausfälle und Verlauf“
  (Ausfälle 24 h/7/30 Tage, Ausfallzeit, Verfügbarkeit, Latenz, Paketverlust, Internet über 7 Tage), die
  Geschwindigkeit ein eigenes Fenster mit Verlauf. Dafür sind weder Bubble Card noch Vorlagen nötig.
- Eigene Ziele (`lines: WANx: tap:`) haben weiter Vorrang vor dem eingebauten Fenster.
- **Geschwindigkeit in der Karte:** kompakte Karte zeigt „↓ … · ↑ … Mbit/s“ als Kennzahl, die volle Karte als Zeile.
- **Mini-Karte ohne Einstellungen:** Ohne eigene Sensoren nimmt sie die Geschwindigkeit aus den Optionen für Verlauf
  und zweite Zeile (jetzt mit ↓ und ↑). `type: custom:homelines-mini` reicht.
- **Fenster übereinander:** Detailfenster lassen sich auch aus der großen Karte im Popup der Mini-Karte öffnen;
  Zurück-Taste und Esc schließen jeweils nur das oberste Fenster.
- Leitungen tragen im Snapshot `primary` (Hauptleitung); der Snapshot enthält die Detail-Einstellungen und die
  Entitäts-IDs von HomeLines selbst (auch bei mehreren Einrichtungen richtig).
- Vorhandene Karten und Dashboards funktionieren unverändert weiter.
- Tests: `test_details_080.py` (Optionen, Snapshot, Detailfenster in Chromium, Mini-Karte mit Sensoren aus den
  Optionen, gestapelte Fenster mit Zurück und Esc).

## 0.7.1 – Karten ohne YAML einrichten
- **Grafische Editoren für alle drei Karten:** Große Karte, Mini-Karte und Kachel lassen sich jetzt im Dashboard-Editor
  per Formular einstellen (Sensoren aus Listen, Vorlagen mit Prüfung, Symbolauswahl). Vorhandenes YAML bleibt gültig;
  Einstellungen, die der Editor nicht kennt (z. B. `popup_cards`, `grid_options`), bleiben erhalten und lassen sich
  weiter im Code-Editor bearbeiten. Geleerte Felder werden aus der Konfiguration entfernt.
  - Mini-Karte: Darstellung (Kachel oder Leiste), Name, Download-/Upload-Sensor und Zeitraum für den Verlauf, eigene
    zweite Zeile, Ziel beim Antippen (Pfad, Dashboard-Seite als Popup, Spalten, HomeLines-Karte im Popup).
  - Große Karte: Titel, kompakt, je Leitung Name nur für diese Karte, Ziel beim Antippen, Zusatzzeile, in der
    Mini-Karte ausblenden. Die Leitungen kommen aus HomeLines.
  - Kachel: Name, Symbol, Text, Bedingungen für Gelb und Rot, Ziel beim Antippen, Entität.
- **Leitungsnamen zentral:** In *HomeLines → Konfigurieren → Leitungen* gibt es „Name für WAN1“ bis „WAN4“. Diese
  Namen gelten in allen HomeLines-Karten; der `lines:`-Block mit `name:` in jeder Karte ist nicht mehr nötig (bleibt aber
  als Vorrang für eine einzelne Karte möglich). Leer: Name aus dem Router.
- Sensor „Aktive Leitung“ hat das neue Attribut `name` (Anzeigename der aktiven Leitung), z. B. für eigene Vorlagen:
  `{{ state_attr('sensor.homelines_active_wan', 'name') }}`.
- Neue Mini-Karte im Kartenauswahl-Dialog startet als Kachel mit Namen „Internet“.
- Tests: `test_editor_071.py` (Editoren in Chromium mit nachgebautem `ha-form`, zentrale Leitungsnamen, Optionen).

## 0.7.0 – HomeLines: erste Veröffentlichung, neue UniFi-IDs werden erkannt
- **Neuer Name: HomeLines** (vorher LineGuard, nicht öffentlich). Technisch heißt die Integration jetzt `homelines`:
  Entitäten `sensor.homelines_*`, Ereignisse `homelines_*`, Dienste `homelines.*`, Karten `custom:homelines-card`,
  `custom:homelines-mini`, `custom:homelines-tile`, UniFi-Regel „HomeLines Notbetrieb“.
- **Umstieg von LineGuard:** Beim Hinzufügen bietet HomeLines an, eine vorhandene LineGuard-Einrichtung zu übernehmen –
  Einstellungen, Gerätegruppen, Verbrauch und Kosten, Notbetriebe und Ausfallhistorie. Solange LineGuard noch läuft,
  erscheint unter *Reparaturen* ein Hinweis; ist LineGuard entfernt, löscht HomeLines dessen alte Regel „LineGuard
  Notbetrieb“ im Router. Die Verläufe der alten Entitäten (Recorder) werden nicht übernommen.
- **UniFi vergibt neue IDs:** Wird die WAN-Konfiguration oder ein Netz in UniFi neu angelegt, ändert sich dessen
  interne ID. HomeLines merkt sich jetzt zusätzlich Name und WAN-Gruppe, gleicht bei jedem Abruf der Geräteliste ab und
  übernimmt die neue ID still. Lehnt UniFi die Regel mit `InvalidNetworkConfId` ab, holt HomeLines die Liste sofort neu
  und versucht es ein zweites Mal.
- **Klare Meldung statt Router-JSON:** Lässt sich die Hauptleitung nicht zuordnen, steht in der Karte „Hauptleitung
  … in UniFi nicht mehr gefunden“ mit Link zu den Optionen, dazu ein Hinweis unter *Reparaturen*. Andere Router-Fehler
  zeigen nur noch die Fehlerkennung (z. B. `HTTP 400: api.err.…`).
- **Netze, die es nicht mehr gibt,** werden nicht mehr an UniFi geschickt (der Rest der Regel wird gesetzt) und stehen
  in der Karte unter *Geräte → Netze* als „Netz nicht mehr gefunden“ mit Knopf *Entfernen*.
- Die Optionen wählen die Hauptleitung bei geänderter ID automatisch über Gruppe bzw. Namen vor.
- Standardwerte neutral: Anbieter leer, Startguthaben 0 €, Beispiele in Hilfetexten ohne echte Namen und Nummern.
- Tests: `test_ids_migration_070.py` (neue WAN- und Netz-IDs, Wiederholung bei `InvalidNetworkConfId`, fehlende
  Leitung, fehlendes Netz, Übernahme von LineGuard, Hinweis solange LineGuard läuft), `test_version.py`.
