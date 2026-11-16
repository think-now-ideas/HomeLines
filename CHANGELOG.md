# Änderungen

## 0.9.0 – Fenster selbst zusammenstellen, Logo mit Schriftzug
- **Fenster-Baukasten:** Jedes Fenster (Leitungen, Notfall-Strecke, Geschwindigkeit, Ausfälle, eigene Kacheln) lässt sich direkt im Fenster mit **✎ Fenster anpassen** zusammenstellen – ohne YAML. Bausteine: Werte, Grafik, Schalter und Aktionen, Protokoll, Hinweistext, Prüfliste Notfall-Handy; Reihenfolge mit ↑ ↓.
- **Grafiken einstellbar:** Linie, Fläche, Balken oder An/Aus-Streifen; 24 Stunden, 7 oder 30 Tage; Werte zusammen oder je Wert eine Grafik; Farbe je Wert; Grenzlinie mit farbigem Bereich; Min, Max und Ø (zeitlich gewichtet).
- **Warnfarben je Wert** als Satz („Gelb, wenn ein Wert unter 20“); fehlende Entitäten werden als „Wert fehlt“ markiert und lassen sich im Editor neu wählen.
- **Eigene Auswahl für Entitäten** mit Vorschlägen passend zum Baustein, Suche nach Name, Bereich oder ID und Filter nach Bereich.
- **FRITZ!Box-Vorlage:** Telefonie, Heizung (DECT), WLAN-Geräte und Router, gefunden über die Integrationen FRITZ!Box Tools, FRITZ!SmartHome und Ping.
- Angepasste Fenster speichert die Integration (neuer Befehl `homelines/set_windows`, nur für Administratoren, Eingaben werden geprüft); sie gelten für alle Karten. „Eingebautes Fenster“ stellt den Ausgangszustand wieder her.
- **Logo mit Schriftzug** im Kopf der großen Karte; der Schriftzug passt sich hellem und dunklem Design an. Mit eigenem Titel bleibt es beim Haus mit Titel.
- **Euro-Beträge** immer mit zwei Nachkommastellen (z. B. 12,40 €), auch in Werten, Kacheln und Grafiken.
- README: Abschnitt „Fenster selbst zusammenstellen“; Formatfehler im Beispiel zu `homelines.set_details` behoben.

## 0.8.8 – Schalter und Zeitpunkte im Detailfenster wieder sichtbar
- **Fehler behoben:** Im Detailfenster der Leitung (Abschnitt „Neueinwahl“) fehlten seit neueren Home-Assistant-Versionen der Schalter „Tägliche Neueinwahl“ und die Uhrzeit bei „Letzte Neueinwahl“. Die HA-Liste holt sich diese Angaben inzwischen aus der HA-Oberfläche, und das HomeLines-Fenster liegt außerhalb davon.
- HomeLines zeichnet die Bedienzeilen jetzt selbst – Schalter, „Drücken“, Uhrzeit, Auswahl, Zahl und Zeitpunkte („heute 22:42 (vor 3 Minuten)“) – wie seit 0.8.5 schon Werte und Verläufe. Antippen von Symbol oder Name öffnet weiter das HA-Detailfenster.

## 0.8.7 – Router-Fingerabdruck für die SSH-Neueinwahl
- **Sicherheit:** HomeLines merkt sich beim ersten SSH-Verbinden den Fingerabdruck (Hostschlüssel) des Routers und schickt das Passwort danach nur noch an genau dieses Gerät. Bisher wurde der Fingerabdruck nicht geprüft; ein fremdes Gerät im Heimnetz hätte sich als Router ausgeben und das Passwort mitlesen können.
- Meldet sich ein Gerät mit anderem Fingerabdruck, wird die Neueinwahl gesperrt, das Passwort nicht gesendet und unter *Einstellungen → Reparaturen* ein Hinweis angezeigt. Nach einem Zurücksetzen oder Austausch des Routers dort „Neuen Router-Fingerabdruck übernehmen“ bestätigen.
- Die SSH-Prüfung in den Optionen nutzt denselben Fingerabdruck; bei geänderter Adresse oder geändertem Port wird neu gelernt.
- README: neuer Abschnitt „Sicherheit“ (warum die Zertifikatsprüfung zur UniFi-Verbindung standardmäßig aus bleibt).

## 0.8.6 – Übersicht in zwei Spalten, eigene Kacheln in der Karte
- **Übersicht in zwei Spalten:** Notfall-Strecke, Leitungen, Geschwindigkeit und Ausfälle stehen je zur halben
  Breite nebeneinander (auf schmalen Bildschirmen untereinander) statt zu dritt.
- **Eigene Kacheln in der großen Karte:** neue Option `tiles:` mit Kacheln wie bei `custom:homelines-tile`
  (z. B. Strom, Telefon). Sie stehen im selben Raster wie die Übersicht, mit gleichem Rahmen und Warnfarben.
- **Alles im visuellen Editor der Karte:** neuer Abschnitt „Eigene Kacheln in der Karte“ mit vier Plätzen
  (dieselben Felder wie bei der einzelnen Kachel) und „Übersicht: Zeilen ausblenden“ mit je einem Schalter für
  Notfall-Strecke, jede Leitung, Geschwindigkeit und Ausfälle (`overview_hide`). Ist die Übersicht ganz aus,
  bleiben die eigenen Kacheln sichtbar.
- **Kürzere Namen im Detailfenster:** Technische Zusätze in Klammern (Adresse, Netz) und doppelte Gerätenamen
  am Anfang werden weggelassen, z. B. „Router WAN (… / …) Router WAN Status“ → „Router WAN Status“.

## 0.8.5 – Detailfenster wie ein gut gebautes Dashboard
- **Verläufe zusammengefasst:** Werte mit gleicher Einheit stehen in einem Diagramm mit Legende (Name und aktueller
  Wert, Tipp öffnet das HA-Detailfenster), z. B. Sync und Erreichbar, Rauschabstand Download und Upload, Speedtest
  Download und Upload oder alle Leistungsmesser einer Kachel. Zeitraum: 30 Tage für Leitungen und Geschwindigkeit,
  24 Stunden für Latenz und Kacheln (einstellbar). Spitzen bleiben auch bei langen Zeiträumen sichtbar.
- **Kurze Namen:** Gemeinsame Anfänge (z. B. „HomeLines …“, Gerätename des Modems) und gemeinsame Endungen
  (z. B. „… Leistung“) werden weggelassen.
- **Notfall-Strecke:** Prüfliste des Notfall-Handys (meldet sich, USB-Kabel mit Akku, Mobilfunk mit Netz und Signal,
  mobile Daten, WLAN) mit Ampelpunkten, Knöpfe „Testmeldung senden“ und „Verbrauch zurücksetzen“, Zeitleiste
  „Notbetrieb – 30 Tage“.
- **Ausfälle und Verlauf:** zusätzlich Router-Status und letzte Prüfung, **Protokoll** der letzten Ausfälle (Beginn,
  Dauer, Ursache), Zeitleiste „Verbindung – 24 Stunden“ (Internet, Router, Hauptleitung, aktive Leitung,
  Betriebsart), Latenz – 24 Stunden, Paketverlust – 30 Tage.
- **Neue Option „Ausfälle: weitere Werte“** (`monitor_extra`, auch in `homelines.set_details`), z. B. die
  Latenz-Messung des Routers; sie erscheint als Feld und im Latenz-Diagramm.
- Leitungen ohne Detailwerte zeigen einen Hinweis statt eines leeren Fensters.
- Leitungskachel zeigt ohne eigene Zusatzzeile die Bandbreite aus den Detailwerten (z. B. „253 · 46 Mbit/s“);
  die Übersichtszeile einer Leitung die ersten zwei Detailwerte (Reihenfolge wie in den Optionen).
- Geprüft gegen ein echtes Home Assistant mit Frontend.

## 0.8.4 – Übersicht zurück, Detailfenster mit echten Werten, Kachel ohne Code
- **Übersicht in der großen Karte:** unter den Kennzahlen je eine Zeile für Notfall-Strecke (Handy, Akku, weitere
  Werte), jede Leitung mit Detailwerten (z. B. „DSL – SHOWTIME · 250 Mbit/s · 46 Mbit/s“), Geschwindigkeit und
  Ausfälle, mit Gelb/Rot bei Problemen. Ein Tipp öffnet das passende Fenster. Abschaltbar im Editor
  („Übersicht zeigen“, `overview: false`).
- **Detailfenster zeichnet HomeLines jetzt selbst:** Werte als Felder mit Namen und Wert, Verläufe als Linien (bzw.
  An/Aus-Streifen), Schalter und Buttons als Bedienliste (z. B. Neueinwahl, „Speedtest starten“). In 0.8.0–0.8.3.1
  zeigten die eingebetteten HA-Kacheln in echten Installationen keine Werte und der Verlauf blieb leer.
  Ein Tipp auf einen Wert öffnet das normale HA-Detailfenster der Entität; das HomeLines-Fenster tritt solange zur Seite.
- **Kachel ohne Vorlagen:** `homelines-tile` zeigt jetzt Werte gewählter Entitäten (`entities`) als Summe, Einzelwert,
  Liste, Durchschnitt, Minimum oder Maximum (`combine`). Warnfarben per Formular: gelb bei nicht erreichbarer Entität
  (`warn_unavailable`), gelb/rot unter/über einem Wert (`warn_below`, `warn_above`, `error_below`, `error_above`).
  Ein Tipp öffnet ein Fenster mit allen Werten und dem Verlauf (`hours`, Standard 24). Vorlagen (`text`, `warning`,
  `error`) gibt es weiter unter „Erweitert“ und haben Vorrang.
- Hauptleitung wird auch ohne UniFi erkannt (erste Leitung mit Status-Sensor, die nicht Backup ist).
- Fenster liegen über der HA-Kopfleiste; Esc schließt kein HomeLines-Fenster, solange ein HA-Detailfenster offen ist.
- Neu im Repo: `examples/` mit Beispiel-Seite, Mini-Karte und Aktion für die Detailansichten.
- Geprüft gegen ein echtes Home Assistant mit Frontend (Seite, Fenster, HA-Detailfenster, Kachel-Editor).

## 0.8.3.1 – Korrektur Übersetzung
- Hilfetext der Aktion `homelines.set_details` ohne geschweifte Klammern (Home Assistant hielt das Beispiel für einen
  Platzhalter; die Prüfung hassfest schlug fehl). Neuer Test prüft alle Übersetzungen darauf.

## 0.8.3 – Detailansichten per Aktion setzen
- **Neue Aktion `homelines.set_details`:** setzt Leitungsnamen, Werte und Verlauf je Leitung, Geschwindigkeit und
  weitere Werte der Notfall-Strecke in einem Schritt – praktisch beim Umstellen oder zum Übertragen auf ein zweites
  System (*Entwicklerwerkzeuge → Aktionen*). Ergebnis wie im Formular *Konfigurieren → Leitungen / Detailansichten*;
  ohne `replace` werden nur die genannten Werte geändert, andere Optionen bleiben unberührt.

## 0.8.2 – Logo
- **HomeLines hat ein Logo:** Symbol und Schriftzug für helle und dunkle Oberflächen unter
  `custom_components/homelines/brand/` (`icon`, `logo`, `dark_icon`, `dark_logo`, je einfach und `@2x`). Home Assistant
  zeigt es bei der Integration unter *Geräte & Dienste* an, die README oben auf GitHub.
- Die große Karte zeigt im Kopf das Haus-Symbol aus dem Logo statt des allgemeinen Symbols.

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
