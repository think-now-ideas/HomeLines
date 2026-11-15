# Änderungen

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
