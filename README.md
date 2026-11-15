# HomeLines – Internet Monitor & Mobile Failover

HomeLines für Home Assistant fasst drei Dinge in einer Integration zusammen:

1. **Internet-Überwachung**: Pings, Ausfallprotokoll, Verfügbarkeit, Latenz.
2. **Geplante Neueinwahl**: verlegt die Zwangstrennung des Providers auf eine ruhige Uhrzeit.
3. **Mobiler Notbetrieb**: Fällt die Hauptleitung aus, dürfen nur ausgewählte Geräte über Mobilfunk. Nach dem Buchen der Tagesflat gibst du per Knopf weitere frei – mit Timer und automatischer Rückkehr.

Dazu gehört eine eigene Dashboard-Karte.

Alles läuft lokal in Home Assistant, ohne Cloud. Die Oberfläche ist auf Deutsch.

## Installation

**Über HACS (empfohlen)**

1. HACS → ⋮ → *Benutzerdefinierte Repositories* → `https://github.com/think-now-ideas/HomeLines`, Typ **Integration**.
2. HomeLines herunterladen und Home Assistant neu starten.
3. *Einstellungen → Geräte & Dienste → Integration hinzufügen → HomeLines*.

**Von Hand:** Den Ordner `custom_components/homelines` nach `/config/custom_components/` kopieren (z. B. mit dem
Samba-Add-on), Home Assistant neu starten, Integration hinzufügen.

Updates zeigt HACS an. Die Karte wird bei jedem Update automatisch neu geladen; zeigt die App noch die alte Version,
in der Companion App *Einstellungen → Companion App → Fehlerbehebung → Frontend-Cache zurücksetzen*.

### Umstieg von LineGuard

HomeLines hieß vor 0.7.0 LineGuard. Ist noch eine LineGuard-Einrichtung vorhanden, fragt HomeLines beim Hinzufügen,
ob es sie übernehmen soll – mit Einstellungen, Gerätegruppen, Zählern und Ausfallhistorie.

1. HomeLines installieren, neu starten, *Integration hinzufügen → HomeLines → Von LineGuard übernehmen*.
2. LineGuard unter *Einstellungen → Geräte & Dienste* löschen und den Ordner `custom_components/lineguard` entfernen,
   dann neu starten. Bis dahin steht unter *Reparaturen* ein Hinweis.
3. HomeLines löscht anschließend die alte Regel „LineGuard Notbetrieb“ im Router.
4. Dashboards umstellen: `custom:lineguard-…` → `custom:homelines-…`, `sensor.lineguard_…` → `sensor.homelines_…`,
   Ereignisse `lineguard_…` → `homelines_…` in Automationen.

## Einrichtung

**1. Router-Anbindung**

| Anbindung | Wofür | Sperre |
|---|---|---|
| UniFi | UDR/UDM/UCG mit Network 9/10 | HomeLines pflegt die Policy-Based Route „HomeLines Notbetrieb“ (Hauptleitung + Kill Switch). Die Regel bleibt dauerhaft gesetzt und greift sofort beim Ausfall, auch wenn HA gerade hängt. |
| Schalter je Gerät | z. B. FRITZ!Box-Integration (Internetzugang je Gerät) | Schaltet die Schalter nur im Notbetrieb aus. |
| Eigene Skripte | jeder andere Router | Ruft deine Skripte mit den Variablen `devices` und `macs` auf und löst das Ereignis `homelines_block` aus. |
| Keine Sperre | nur Überwachung, Timer und Kosten | – |

UniFi-API-Schlüssel: *UniFi → Einstellungen → Control Plane → Integrationen → API-Schlüssel erstellen*.

**2. Leitungen**

*Bereitschaft der Backup-Leitung*

- **Warm**: Die Backup-Leitung ist ständig verbunden, der Router schaltet selbst um (z. B. UniFi-Gateway mit Backup-WAN). Der Router prüft sie dabei laufend, das braucht etwas Datenvolumen.
- **Kalt**: Die Backup-Leitung ist im Alltag ganz aus (Tethering aus, mobile Daten aus, Handy im WLAN) – kein Byte über die SIM. Fällt die Hauptleitung aus, meldet HomeLines das und führt mit einem **Assistenten in der Karte** durch die Schritte: Tagesflat buchen und freischalten → WLAN am Handy aus → mobile Daten an → USB-Kabel → Tethering an. Jeder Schritt wird live geprüft. Ist die Hauptleitung zurück, erinnert der Assistent an den Rückweg (Tethering aus, mobile Daten aus, WLAN an), damit nichts weiter über die SIM läuft. Für die WLAN-Prüfung den Sensor „Wi-Fi connection“ der HA-App unter *Optionen → Handy* wählen.

*Ausfall der Hauptleitung erkennen über*

| Art | Wofür |
|---|---|
| Aktive Leitung | UniFi: `sensor.unifi_active_wan_id` |
| Status der Hauptleitung | Binärsensor, an = verbunden (z. B. FRITZ!Box „Verbindung“, UniFi „WAN2 Internet“) – für kalte Bereitschaft mit UniFi am besten geeignet |
| Eigener Sensor | eigener Template-/Binärsensor, an = Hauptleitung weg |
| Eigene Pings | ohne passenden Sensor: HomeLines pingt selbst. Antwortet der Router, das Internet aber nicht, ist die Leitung weg. |

„Ausfall gilt als echt nach“ ignoriert kurze Aussetzer (Standard 0 s warm, 180 s kalt).

*Weitere Felder*

- Sensor für die aktive Leitung: `sensor.unifi_active_wan_id` (UniFi-WAN-Integration)
- Backup-Leitung: `WAN3`
- Status-Sensoren: die „Internet“-Binärsensoren je WAN
- Speedtest-Schalter: `switch.unifi_wan_auto_speedtest` – wird im Notbetrieb automatisch aus- und danach wieder eingeschaltet
- Hauptleitung für die Sperrregel: z. B. `DSL (WAN2)`. Legt UniFi die Leitung neu an (neue interne ID), findet HomeLines sie über Name und WAN-Gruppe wieder; klappt das nicht, steht ein Hinweis in der Karte und unter *Reparaturen*.
- Gruppe für neue Geräte: Standard „Mit Tagesflat“

**3. Neueinwahl (optional)**

- **SSH** (UniFi, teils OpenWrt): SSH-Daten des Routers, Schnittstelle `ppp1`, Uhrzeit `04:00`.
- **HA-Button oder Skript** (jeder Router, z. B. FRITZ!Box-Button „Neu verbinden“): Auslöser wählen, optional einen Sensor mit der öffentlichen IP zur Erfolgskontrolle.

Danach in den **Optionen** (Zahnrad der Integration):

- **Tarif und Kosten**: Anbieter, Preis je MB (z. B. 3 ct), Tagesflat (z. B. 7,99 € / 24 h), Puffer, Startguthaben, Link zur Buchung
- **Handy**: `Mobile Rx GB`, `Mobile Tx GB`, `Mobile data`, `Data network type (SIM 1)`, `Signal strength (SIM 1)`, `SIM 1`, `Battery level`, `Charger type`
- **Weckruf** (ab 0.5.0): Unter *Optionen → Handy* den Benachrichtigungsdienst der App am Handy wählen (z. B. `notify.mobile_app_notfall_handy`). Die App sendet nur geänderte Werte, und Android bremst Apps im Hintergrund. HomeLines schickt deshalb `command_update_sensors`, wenn das Handy länger als die eingestellte Zeit (Standard 10 min) still war, und sofort, wenn der Notbetrieb beginnt. Als Lebenszeichen zählt jede Entität des Handy-Geräts, z. B. auch die WLAN-Signalstärke. Am Handy: Akku für die HA-App auf „Nicht eingeschränkt“, dauerhafte Verbindung „Im Heim-WLAN“.
- **Benachrichtigungen**: Empfänger anlegen und festlegen, welche Meldung an wen geht (siehe unten)
- **Internet-Überwachung**: Ping-Ziele, Router-IP, Intervall (im Notbetrieb automatisch seltener, das spart Volumen)

## Benachrichtigungen

*Optionen → Benachrichtigungen* hat drei Punkte:

- **Empfänger hinzufügen**: Name, Benachrichtigungsdienst und optional Empfänger.
  - **HA-App**: z. B. `notify.mobile_app_mein_handy`, Empfänger leer lassen.
  - **E-Mail**: Die Adressen legst du in der SMTP-Integration an (*Einstellungen → Geräte & Dienste → SMTP → Empfänger hinzufügen*). Jede Adresse ist dort eine eigene Entität, z. B. `notify.smtp_alex`, die du hier wählst.
  - **SMS**: Den SMS-Dienst richtest du als eigene Integration ein. Braucht er die Nummer bei jeder Nachricht, trägst du sie hier als Empfänger ein, z. B. `+49 123 4567890` (mehrere mit Komma). „Als kurze Textnachricht“ fasst Titel und Text zu einer Zeile zusammen.
- **Empfänger bearbeiten oder löschen**
- **Welche Meldung an wen**: je Meldung die Empfänger ankreuzen, keiner angekreuzt = aus.

| Meldung | Wann |
|---|---|
| Notbetrieb beginnt | Hauptleitung ausgefallen (bei der geplanten Neueinwahl erst nach 3 Minuten) |
| Tagesflat endet in 15 Minuten | vor der Rückschaltung |
| Zurück im Notbetrieb | Freigabe abgelaufen |
| Hauptleitung wieder da | mit Dauer des Notbetriebs |
| Backup-Leitung ausgefallen / wieder bereit | Internet läuft, aber die Backup-Leitung ist länger als eingestellt (Standard 10 min) weg |
| Notfall-Handy meldet sich nicht | länger als eingestellt keine Werte von der HA-App |
| Neueinwahl fehlgeschlagen | tägliche Neueinwahl ohne Wirkung oder mit Fehler |

**Wenn das Internet ganz weg ist** (kalte Bereitschaft), kommen Push über Apple/Google, E-Mail und Internet-SMS nicht an. Dafür gibt es Wege ohne Internet:
- **HA-App mit lokaler Push**: In der App unter *Einstellungen → Companion App → Server → Heimnetzwerk/WLAN-SSIDs* das Heim-WLAN eintragen; dann kommen Meldungen dort direkt über Home Assistant an.
- **`persistent_notification.create`**: Meldung direkt in Home Assistant.
- **Skripte** als Empfänger: z. B. eine Ansage auf Lautsprechern oder ein blinkendes Licht. Das Skript bekommt `title`, `message`, `text` und `recipient`.
- **SMS über einen GSM-Stick** am HA-Rechner.

Mit dem Button **Testmeldung senden** prüfst du alle Empfänger auf einmal. Push, E-Mail und SMS über Internetdienste brauchen im Notbetrieb selbst Internet; deshalb kommt Home Assistant automatisch in die Gruppe „Immer“.

## Gruppen

| Gruppe | Hauptleitung weg | Mit Tagesflat |
|---|---|---|
| Immer | online | online |
| Mit Tagesflat | gesperrt | online |
| Nie | gesperrt | gesperrt |

Zuordnen geht für einzelne Geräte und (bei UniFi) für ganze Netze, am bequemsten in der Karte über **Geräte**. Netze, die es in UniFi nicht mehr gibt, stehen dort als „Netz nicht mehr gefunden“ und werden nicht an den Router geschickt. Ein Gerät ohne eigene Zuordnung erbt die Gruppe seines Netzes, sonst die Standardgruppe. **Home Assistant selbst kommt automatisch in „Immer“**, damit Meldungen im Notbetrieb durchkommen.

## Karte

Dashboard bearbeiten → *Karte hinzufügen* → **HomeLines**, **HomeLines Mini** oder **HomeLines Kachel**. Alle drei
Karten haben einen grafischen Editor; YAML ist nur für Sonderfälle nötig (z. B. weitere Karten im Popup). Die Karten
werden automatisch geladen, eine Ressource musst du nicht anlegen.

**Leitungsnamen** wie „Glasfaser“, „DSL“ oder „5G Backup“ stellst du einmal unter *HomeLines → Konfigurieren →
Leitungen* ein („Name für WAN1“ …). Sie gelten in allen Karten. Für eigene Vorlagen steht der Name der aktiven Leitung
im Attribut `name` von `sensor.homelines_active_wan`.

Die YAML-Beispiele unten zeigen alle Einstellungen:

```yaml
type: custom:homelines-card
```

**Kompakt und mit Leitungskacheln** (ab 0.4.0):

```yaml
type: custom:homelines-card
compact: true          # im Normalbetrieb nur Kopf, Leitungen und Kennzahlen
lines:                 # optional, je Leitung nur für diese Karte
  WAN1:
    tap: "#glasfaser"  # Klickziel: Unterseite (/dashboard/seite) oder Bubble-Card-Popup (#hash)
  WAN2:
    tap: "#dsl"
    info: "↓ {{ states('sensor.modem_dsl_downstream') | int }} Mbit/s"   # Vorlage
  WAN3:
    name: Notfall      # überschreibt den Namen aus den Optionen nur in dieser Karte
    tap: "#notfall"    # ohne info zeigt die Backup-Leitung den Zustand des Notfall-Handys
```

Im Notbetrieb zeigt die kompakte Karte automatisch Assistent, Timer, Kosten und Notfall-Kette.

**Mini-Karte** `custom:homelines-mini` (ab 0.5.0) – Statusleiste oder kleine Kachel für die Startseite. Ampelfarbe, aktive Leitung, Durchsatz-Verlauf und Leitungspunkte; im Notbetrieb „X von Y online · MB · €“. Ein Klick öffnet die große Karte als Popup.

```yaml
type: custom:homelines-mini
layout: bar                 # oder tile
name: Internet
throughput_entity: sensor.wan_download   # optional: Verlauf als Sparkline
upload_entity: sensor.wan_upload         # optional: zweite Linie (blau)
throughput_hours: 6
info: "{{ … }}"             # optional: eigene zweite Zeile im Normalbetrieb
navigation_path: "#internet"  # optional: statt des eingebauten Popups
popup_view: /dashboard-beispiel/internet   # optional (ab 0.6.1): vorhandene Dashboard-Seite als Modal
popup_cards:                # optional (ab 0.6.0): weitere Karten im Popup, z. B. Detail-Kacheln
  - type: custom:homelines-tile
    name: DSL
    text: "{{ states('sensor.x') }}"
    navigation_path: "#dsl"   # öffnet ein Bubble-Popup; das HomeLines-Popup tritt solange zur Seite
popup_columns: 2
card:                       # optional: Einstellungen der großen Karte im Popup
  compact: true
```

Alle HomeLines-Karten teilen sich eine Datenverbindung. Nach einem Neustart von Home Assistant zeigen sie „Verbinde mit HomeLines …“ und versuchen es alle paar Sekunden erneut, bis die Integration geladen ist.

**Kachel mit Warnfarben** `custom:homelines-tile` – für Übersichten mit eigenen Vorlagen:

```yaml
type: custom:homelines-tile
name: Telefon
icon: mdi:phone-classic
navigation_path: "#telefon"
text: "{{ states('sensor.telefon_status') }}"
warning: "{{ states('sensor.x') | float(0) < 20 }}"   # gelb
error: "{{ is_state('sensor.y', 'not registered') }}"  # rot
```

Optional: `title: Internet`, `entry_id: …` (bei mehreren HomeLines-Einträgen).

## Entitäten

**Notbetrieb**: Status, Aktive Leitung (mit allen Leitungen als Attribut), Rückschaltung, Tagesflat endet, Geräte online, Binärsensor Notbetrieb, Notfall-Handy meldet sich, Router-Anbindung gestört.
**Kosten**: Mobilfunk-Verbrauch (MB seit Reset), Mobilfunk-Kosten, Guthaben (geschätzt).
**Überwachung**: Internet, Router (wenn Router-IP gesetzt), Latenz, Paketverlust, Ausfälle 24 h / 7 / 30 Tage, Ausfallzeit 7 Tage, Verfügbarkeit 7 / 30 Tage, Letzter Ausfall (Attribut `recent_outages` mit den letzten 20).
**Neueinwahl**: WAN-IP, Letzte Neueinwahl, Ergebnis Neueinwahl, Schalter Tägliche Neueinwahl, Uhrzeit Neueinwahl.
**Buttons**: Tagesflat freischalten, Wieder einschränken, Verbrauch zurücksetzen, Testmeldung senden, Jetzt neu verbinden.

## Dienste und Ereignisse

Dienste: `homelines.activate_dayflat` (optional `booked_at`), `homelines.restrict`, `homelines.set_group`, `homelines.reset_usage` (optional `start_balance`), `homelines.reconnect`, `homelines.test_notify`.

Ereignisse: `homelines_mode_changed`, `homelines_outage_started`, `homelines_outage_ended`, `homelines_reconnected`, `homelines_block`.

## Hinweise

- Die geplante Neueinwahl löst kurz einen Failover aus. HomeLines weiß das und meldet dafür keinen Notbetrieb.
- Kosten sind eine Schätzung aus den Handy-Zählern. Verbindlich ist die Abrechnung des Anbieters.
- Beim Löschen der Integration entfernt HomeLines seine UniFi-Regel wieder.
- Verbrauchszähler werden anhand ihrer Einheit umgerechnet (GB, MB, kB …). Damit lassen sich auch Router mit eigenem Mobilfunk-Zähler nutzen.

## Entwicklung

Tests: `pip install pytest-homeassistant-custom-component asyncssh icmplib`, dann `pytest`.
Übersetzungen werden mit `python tools/build_translations.py` erzeugt (nicht von Hand bearbeiten).
Die Version steht in `manifest.json`, `const.py` und der Karte (`HL_VERSION`); ein Test prüft, dass sie gleich sind.
Änderungen stehen in [CHANGELOG.md](CHANGELOG.md).

## Lizenz

MIT
