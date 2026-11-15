"""Erzeugt strings.json und translations/{de,en}.json."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "custom_components" / "homelines"


def t(de, en):
    return {"de": de, "en": en}


LINES = {
    "standby": t("Bereitschaft der Backup-Leitung", "Backup line standby"),
    "detection": t("Ausfall der Hauptleitung erkennen über", "Detect main line failure via"),
    "primary_status_entity": t("Status-Sensor der Hauptleitung", "Main line status sensor"),
    "custom_down_entity": t("Eigener Sensor „Hauptleitung weg“", "Custom “main line down” sensor"),
    "detect_delay": t("Ausfall gilt als echt nach", "Failure counts as real after"),
    "active_wan_entity": t("Sensor für die aktive Leitung", "Active line sensor"),
    "backup_wan": t("Backup-Leitung (Mobilfunk)", "Backup line (cellular)"),
    "wan_status_entities": t("Status-Sensoren der Leitungen", "Line status sensors"),
    "speedtest_switch": t("Schalter für automatischen Speedtest", "Automatic speedtest switch"),
    "primary_wan_network": t("Hauptleitung für die Sperrregel", "Primary line for the block rule"),
    "default_group": t("Gruppe für neue Geräte", "Group for new devices"),
    **{f"line_name_wan{i}": t(f"Name für WAN{i}", f"Name for WAN{i}") for i in range(1, 5)},
}
DETAILS = {
    **{k: v for i in range(1, 5) for k, v in (
        (f"details_wan{i}", t(f"WAN{i}: Werte", f"WAN{i}: values")),
        (f"history_wan{i}", t(f"WAN{i}: Verlauf", f"WAN{i}: history")))},
    "speed_download": t("Geschwindigkeit: Download-Sensor", "Speed: download sensor"),
    "speed_upload": t("Geschwindigkeit: Upload-Sensor", "Speed: upload sensor"),
    "backup_extra": t("Notfall-Strecke: weitere Werte", "Backup line: more values"),
}
DETAILS_DESC = {
    **{k: v for i in range(1, 5) for k, v in (
        (f"details_wan{i}", t("Als Kacheln im Fenster der Leitung, z. B. Sync, Rauschabstand oder Status des Modems.", "Shown as tiles.")),
        (f"history_wan{i}", t("Als Diagramm der letzten 7 Tage.", "Shown as 7-day graph.")))},
    "speed_download": t("Z. B. der Speedtest-Sensor des Routers. Die Mini-Karte zeigt ihn als Verlauf, wenn dort nichts anderes eingestellt ist.",
                        "E.g. the router's speedtest sensor. Used by the mini card by default."),
    "speed_upload": t("Zweite Linie im Verlauf.", "Second line in the graph."),
    "backup_extra": t("Z. B. Stromverbrauch des Notfall-Routers. Handy, Verbrauch und Kosten zeigt HomeLines dort von selbst.",
                      "E.g. power of the backup router."),
}
LINES_DESC = {
    **{f"line_name_wan{i}": t("Optional. So heißt die Leitung in allen HomeLines-Karten, z. B. „Glasfaser“, „DSL“ oder „5G Backup“. Leer: Name aus dem Router.",
                              "Optional. Shown in all HomeLines cards. Empty: name from the router.") for i in range(1, 5)},
    "standby": t("Warm: Backup ist ständig verbunden, der Router schaltet selbst um. Kalt: Backup ist aus und wird im Ausfall von Hand eingeschaltet – HomeLines führt dich mit einem Assistenten durch die Schritte.",
                 "Warm: backup always connected, router fails over itself. Cold: backup off, switched on by hand with a guided assistant."),
    "detection": t("Warme Bereitschaft mit UniFi: „Aktive Leitung“. Kalte Bereitschaft (der Router kann nicht selbst umschalten) und FRITZ!Box: „Status der Hauptleitung“, z. B. „UniFi WAN2 Internet“ oder der FRITZ!Box-Sensor „Verbindung“. Ohne passenden Sensor: „Eigene Pings“.",
                   "UniFi: active line. FRITZ!Box: main line status. Without a sensor: own pings."),
    "primary_status_entity": t("An = Hauptleitung verbunden. Wird bei „Aktive Leitung“ zusätzlich genutzt, falls gesetzt.", "On = main line connected."),
    "custom_down_entity": t("An = Hauptleitung weg. Für eigene Template-Sensoren.", "On = main line down."),
    "detect_delay": t("Kurze Aussetzer wie die Zwangstrennung werden ignoriert. Leer: 0 s bei warmer, 180 s bei kalter Bereitschaft.",
                      "Short dropouts are ignored. Empty: 0 s warm, 180 s cold."),
    "active_wan_entity": t("Zum Beispiel „UniFi Active WAN ID“ aus der UniFi-WAN-Integration.",
                           "For example “UniFi Active WAN ID” from the UniFi WAN integration."),
    "backup_wan": t("So, wie der Sensor die Mobilfunkleitung nennt, etwa WAN3.", "As the sensor names it, e.g. WAN3."),
    "wan_status_entities": t("Für die Anzeige oben in der Karte, ein Sensor je Leitung.",
                             "Shown at the top of the card, one per line."),
    "speedtest_switch": t("Wird im Notbetrieb ausgeschaltet, damit kein Speedtest das Datenvolumen verbraucht.",
                          "Switched off during backup operation so no speedtest uses up data."),
    "primary_wan_network": t("Geräte, die gesperrt sind, dürfen nur über diese Leitung ins Internet.",
                             "Blocked devices may only use this line."),
    "default_group": t("Gilt für Geräte, die HomeLines neu im Netz entdeckt.", "Applies to devices HomeLines newly discovers."),
}
MONITOR = {
    "targets": t("Ping-Ziele (kommagetrennt)", "Ping targets (comma separated)"),
    "router_ip": t("IP-Adresse des Routers (für die Ursache)", "Router IP (to tell the cause)"),
    "interval": t("Prüfintervall", "Check interval"),
    "emergency_interval": t("Prüfintervall im Notbetrieb", "Interval during backup operation"),
    "ping_count": t("Pings je Ziel", "Pings per target"),
    "failures_before_offline": t("Fehlversuche bis „offline“", "Failures before offline"),
}
TARIFF = {
    "provider": t("Anbieter", "Provider"),
    "price_per_mb": t("Preis ohne Tagesflat", "Price without day pass"),
    "included_mb": t("Inklusiv-Volumen", "Included data"),
    "dayflat_price": t("Preis der Tagesflat", "Day pass price"),
    "dayflat_hours": t("Dauer der Tagesflat", "Day pass duration"),
    "buffer_minutes": t("Sicherheitspuffer", "Safety buffer"),
    "start_balance": t("Startguthaben", "Starting balance"),
    "booking_url": t("Link zum Buchen der Tagesflat", "Link to book the day pass"),
}
TARIFF_DESC = {
    "buffer_minutes": t("So viel früher schaltet HomeLines zurück, bevor die Tagesflat endet.",
                        "HomeLines switches back this much earlier than the day pass ends."),
    "start_balance": t("Guthaben beim letzten Zurücksetzen des Zählers.", "Balance at the last counter reset."),
    "booking_url": t("Wird in der Karte als Knopf angezeigt, z. B. die Aufladeseite deines Anbieters",
                     "Shown as a button in the card."),
}
PHONE = {
    "phone_rx": t("Empfangene Daten (Mobile Rx GB)", "Received data (Mobile Rx GB)"),
    "phone_tx": t("Gesendete Daten (Mobile Tx GB)", "Sent data (Mobile Tx GB)"),
    "phone_mobile_data": t("Mobile Daten an/aus", "Mobile data on/off"),
    "phone_network": t("Netztyp (z. B. Data network type)", "Network type"),
    "phone_signal": t("Signalstärke", "Signal strength"),
    "phone_operator": t("Netzbetreiber (SIM 1)", "Operator (SIM 1)"),
    "phone_battery": t("Akkustand", "Battery level"),
    "phone_charger": t("Ladeart (Charger type)", "Charger type"),
    "phone_wifi": t("WLAN-Verbindung (Wi-Fi connection)", "Wi-Fi connection"),
    "phone_stale_minutes": t("Handy gilt als stumm nach", "Phone counts as silent after"),
    "phone_notify": t("Weckruf über (App-Benachrichtigung des Handys)", "Wake-up via (phone's app notification)"),
    "phone_wake_minutes": t("Wecken, wenn still seit", "Wake when silent for"),
}
PHONE_DESC = {
    "phone_notify": t("z. B. notify.mobile_app_notfall_handy. HomeLines bittet die App damit, alle Sensoren sofort zu senden – "
                      "nur wenn das Handy länger still war und sofort beim Notbetrieb. Leer = kein Weckruf.",
                      "Asks the app to send all sensors now – only when the phone was quiet and immediately on emergency."),
    "phone_wake_minutes": t("Kein erneutes Wecken innerhalb dieser Zeit.", "No repeated wake-up within this time."),
}
TARGET = {
    "label": t("Name", "Name"),
    "service": t("Benachrichtigungsdienst", "Notification service"),
    "recipient": t("Empfänger (optional)", "Recipient (optional)"),
    "sms": t("Als kurze Textnachricht (für SMS)", "As short text (for SMS)"),
    "remove": t("Diesen Empfänger löschen", "Remove this recipient"),
}
TARGET_DESC = {
    "label": t("Wie der Empfänger in HomeLines heißt, z. B. „SMS an Alex“.", "How the recipient is called in HomeLines."),
    "service": t("HA-App, E-Mail (je Empfänger eine Entität der SMTP-Integration), SMS-Dienst, Telegram … Ohne Internet funktionieren: HA-App mit lokaler Push im Heim-WLAN, „persistent_notification.create“ (Meldung in HA) und Skripte (z. B. Ansage oder blinkendes Licht; sie bekommen title, message und text).",
                 "HA app, email (one SMTP entity per recipient), SMS service, Telegram … Custom names can be typed."),
    "recipient": t("Nur nötig, wenn der Dienst die Nummer bei jeder Nachricht braucht, z. B. +49 123 4567890. Mehrere mit Komma trennen.",
                   "Only if the service needs the recipient per message, e.g. +49 123 4567890. Separate several with commas."),
    "sms": t("Titel und Text werden zu einer Zeile zusammengefasst.", "Title and text are merged into one line."),
}
MSGS = {
    "emergency": t("Notbetrieb beginnt", "Backup operation starts"),
    "flat_warning": t("Tagesflat endet in 15 Minuten", "Day pass ends in 15 minutes"),
    "flat_expired": t("Zurück im Notbetrieb (Freigabe abgelaufen)", "Back to backup operation"),
    "restored": t("Hauptleitung wieder da", "Main line restored"),
    "backup_down": t("Backup-Leitung ausgefallen / wieder bereit", "Backup line down / ready again"),
    "phone_silent": t("Notfall-Handy meldet sich nicht", "Backup phone not reporting"),
    "reconnect_failed": t("Neueinwahl fehlgeschlagen", "Reconnect failed"),
    "backup_down_minutes": t("Backup-Leitung gilt als ausgefallen nach", "Backup line counts as down after"),
}
RECONNECT = {
    "reconnect_enabled": t("Tägliche Neueinwahl aktivieren", "Enable daily reconnect"),
    "ssh_host": t("Router-Adresse für SSH", "Router address for SSH"),
    "ssh_port": t("SSH-Port", "SSH port"),
    "ssh_user": t("SSH-Benutzer", "SSH user"),
    "ssh_password": t("SSH-Passwort", "SSH password"),
    "ppp_interface": t("PPP-Schnittstelle", "PPP interface"),
    "reconnect_method": t("Methode", "Method"),
    "reconnect_time": t("Uhrzeit", "Time"),
    "reconnect_entity": t("Auslöser in HA (nur bei Methode „HA-Button oder Skript“)", "HA trigger (method “HA button or script”)"),
    "wan_ip_entity": t("Sensor mit der öffentlichen IP (zur Erfolgskontrolle)", "Public IP sensor (to check success)"),
}
RECONNECT_DESC = {
    "reconnect_entity": t("z. B. der Button „Neu verbinden“ der FRITZ!Box-Integration oder ein eigenes Skript.", "e.g. the FRITZ!Box “Reconnect” button."),
    "wan_ip_entity": t("Optional. Ändert sich die IP oder fällt die Leitung kurz weg, gilt die Neueinwahl als erfolgreich.", "Optional."),
    "ssh_host": t("Nur für die SSH-Methoden.", "SSH methods only."),
}
UNIFI = {
    "host": t("Adresse des UniFi-Routers", "UniFi router address"),
    "api_key": t("API-Schlüssel", "API key"),
    "site": t("Site", "Site"),
    "verify_ssl": t("Zertifikat prüfen", "Verify certificate"),
}
SWITCHES = {"switch_entities": t("Internetzugang-Schalter je Gerät", "Internet access switch per device")}
SCRIPTS = {
    "script_block": t("Skript zum Sperren", "Script to block"),
    "script_unblock": t("Skript zum Freigeben", "Script to unblock"),
    "tracker_entities": t("Geräte (Device Tracker)", "Devices (device trackers)"),
}


def form(title, desc, data, data_desc=None):
    return {"title": title, "description": desc, "data": data, "data_description": data_desc or {}}


def build(lang):
    L = lambda d: {k: v[lang] for k, v in d.items()}  # noqa: E731
    tr = lambda de, en: de if lang == "de" else en  # noqa: E731
    steps = {
        "legacy": {"title": tr("LineGuard gefunden", "LineGuard found"),
                   "description": tr("HomeLines ist der Nachfolger von LineGuard. Du kannst Einstellungen, Gerätegruppen, Zähler und Ausfallhistorie übernehmen. Danach LineGuard entfernen – HomeLines löscht dann die alte Regel im Router.",
                                     "HomeLines succeeds LineGuard. You can take over settings, device groups, counters and outage history. Remove LineGuard afterwards."),
                   "menu_options": {"import_legacy": tr("Von LineGuard übernehmen", "Take over from LineGuard"),
                                    "user": tr("Neu einrichten", "Set up from scratch")}},
        "user": form(tr("HomeLines einrichten", "Set up HomeLines"),
                     tr("Überwacht deine Internetleitungen und steuert den mobilen Notbetrieb. Wähle, wie HomeLines Geräte am Router sperren soll.",
                        "Monitors your internet lines and controls cellular backup. Choose how HomeLines blocks devices at your router."),
                     {"name": tr("Name", "Name"), "router_type": tr("Router-Anbindung", "Router connection")}),
        "unifi": form(tr("UniFi verbinden", "Connect UniFi"),
                      tr("Den API-Schlüssel legst du in UniFi unter Einstellungen → Control Plane → Integrationen an. HomeLines legt dort eine Policy-Based Route „HomeLines Notbetrieb“ an und pflegt sie.",
                         "Create the API key in UniFi under Settings → Control Plane → Integrations. HomeLines creates and maintains a policy-based route “HomeLines Notbetrieb”."),
                      L(UNIFI)),
        "switches": form(tr("Schalter je Gerät", "Switch per device"),
                         tr("Schalter, die den Internetzugang eines Geräts erlauben (an) oder sperren (aus), z. B. aus der FRITZ!Box-Integration.",
                            "Switches that allow (on) or block (off) a device’s internet access, e.g. from the FRITZ!Box integration."),
                         L(SWITCHES)),
        "scripts": form(tr("Eigene Skripte", "Custom scripts"),
                        tr("Die Skripte bekommen die Variablen devices und macs mit den zu sperrenden Geräten.",
                           "Scripts receive the variables devices and macs with the devices to block."),
                        L(SCRIPTS)),
        "lines": form(tr("Leitungen", "Lines"), tr("Woran HomeLines erkennt, welche Leitung gerade aktiv ist.", "How HomeLines tells which line is active."),
                      L(LINES), L(LINES_DESC)),
        "reconnect": form(tr("Geplante Neueinwahl", "Scheduled reconnect"),
                          tr("Optional: Verlegt die Zwangstrennung des Providers auf eine ruhige Uhrzeit. Dafür muss SSH am Router aktiv sein (UniFi → Einstellungen → Control Plane → Konsole → SSH).",
                             "Optional: moves the provider’s forced disconnect to a quiet time. Requires SSH on the router."),
                          L(RECONNECT), L(RECONNECT_DESC)),
    }
    errors = {
        "cannot_connect": tr("Router nicht erreichbar. Adresse prüfen.", "Router not reachable."),
        "invalid_auth": tr("API-Schlüssel abgelehnt.", "API key rejected."),
        "no_wan": tr("Keine WAN-Leitung gefunden.", "No WAN line found."),
        "ssh_missing": tr("Für die Neueinwahl Adresse und SSH-Passwort eintragen.", "Enter address and SSH password."),
        "ssh_auth": tr("SSH-Benutzer oder Passwort falsch.", "Wrong SSH user or password."),
        "ssh_connect": tr("SSH nicht erreichbar. Ist SSH am Router aktiviert?", "SSH not reachable."),
        "invalid_interface": tr("Ungültiger Schnittstellenname.", "Invalid interface name."),
        "entity_missing": tr("Bitte den Auslöser wählen.", "Please choose the trigger."),
        "interface_not_found": tr("Diese PPP-Schnittstelle gibt es auf dem Router nicht.", "PPP interface not found on router."),
    }
    opt_steps = {
        "init": {"title": tr("HomeLines-Optionen", "HomeLines options"),
                 "menu_options": {"lines": tr("Leitungen", "Lines"),
                                  "details": tr("Detailansichten der Karte", "Card detail views"), "tariff": tr("Tarif und Kosten", "Tariff and costs"),
                                  "phone": tr("Handy (Notfall-Modem)", "Phone (backup modem)"),
                                  "notify": tr("Benachrichtigungen", "Notifications"),
                                  "monitor": tr("Internet-Überwachung", "Internet monitor"),
                                  "reconnect": tr("Geplante Neueinwahl", "Scheduled reconnect"),
                                  "router": tr("Router-Anbindung", "Router connection")}},
        "lines": steps["lines"],
        "details": form(tr("Detailansichten der Karte", "Card detail views"),
                        tr("Ein Tipp auf eine Leitung in der HomeLines-Karte öffnet ein Fenster mit diesen Werten und Verläufen – ohne eigene Dashboard-Seite oder Popups. Neueinwahl, Ausfälle und Notfall-Strecke zeigt HomeLines dort von selbst.",
                           "Tapping a line in the HomeLines card opens a window with these values and graphs."),
                        L(DETAILS), L(DETAILS_DESC)),
        "monitor": form(tr("Internet-Überwachung", "Internet monitor"), tr("Pings an mehrere Ziele. Das Internet gilt erst als weg, wenn keines antwortet.", "Pings several targets."), L(MONITOR)),
        "tariff": form(tr("Tarif und Kosten", "Tariff and costs"), tr("Für Kostenrechnung, Guthaben und den Tagesflat-Timer.", "For costs, balance and day pass timer."), L(TARIFF), L(TARIFF_DESC)),
        "phone": form(tr("Handy (Notfall-Modem)", "Phone (backup modem)"),
                      tr("Sensoren aus der Home-Assistant-App des Handys am Notfall-Router. Mobile Rx/Tx zählen die Kosten.",
                         "Sensors from the Home Assistant app on the backup phone."), L(PHONE), L(PHONE_DESC)),
        "notify": {"title": tr("Benachrichtigungen", "Notifications"),
                   "description": tr("Empfänger bisher: {targets}", "Recipients so far: {targets}"),
                   "menu_options": {"notify_add": tr("Empfänger hinzufügen", "Add recipient"),
                                    "notify_pick": tr("Empfänger bearbeiten oder löschen", "Edit or remove recipient"),
                                    "notify_messages": tr("Welche Meldung an wen", "Which message to whom")}},
        "notify_add": form(tr("Empfänger hinzufügen", "Add recipient"),
                           tr("Neue Empfänger bekommen zunächst alle Meldungen. Unter „Welche Meldung an wen“ kannst du das danach einschränken.",
                              "New recipients get all messages at first."), L(TARGET), L(TARGET_DESC)),
        "notify_pick": form(tr("Empfänger wählen", "Choose recipient"), "", {"target": tr("Empfänger", "Recipient")}),
        "notify_edit": form(tr("Empfänger bearbeiten", "Edit recipient"), "", L(TARGET), L(TARGET_DESC)),
        "notify_messages": form(tr("Welche Meldung an wen", "Which message to whom"),
                                tr("Für jede Meldung die Empfänger ankreuzen. Keiner angekreuzt heißt: Meldung aus. Home Assistant muss in der Gruppe „Immer“ sein, damit Meldungen im Notbetrieb durchkommen.",
                                   "Tick recipients per message. None ticked means off."), L(MSGS)),
        "reconnect": steps["reconnect"],
        "router": form(tr("Router-Anbindung", "Router connection"), "", {**L(UNIFI), **L(SWITCHES), **L(SCRIPTS)}),
    }
    entity = {
        "sensor": {
            "status": {"name": tr("Status", "Status"), "state": {"normal": tr("Normalbetrieb", "Normal"), "emergency": tr("Notbetrieb", "Backup operation"), "dayflat": tr("Tagesflat aktiv", "Day pass active")}},
            "active_wan": {"name": tr("Aktive Leitung", "Active line")},
            "restore_at": {"name": tr("Rückschaltung", "Switch back at")},
            "dayflat_end": {"name": tr("Tagesflat endet", "Day pass ends")},
            "devices_online": {"name": tr("Geräte online", "Devices online")},
            "usage": {"name": tr("Mobilfunk-Verbrauch", "Cellular usage")},
            "cost": {"name": tr("Mobilfunk-Kosten", "Cellular costs")},
            "balance": {"name": tr("Guthaben (geschätzt)", "Balance (estimated)")},
            "latency": {"name": tr("Latenz", "Latency")},
            "packet_loss": {"name": tr("Paketverlust", "Packet loss")},
            "outages_24h": {"name": tr("Ausfälle 24 h", "Outages 24 h")},
            "outages_7d": {"name": tr("Ausfälle 7 Tage", "Outages 7 days")},
            "outages_30d": {"name": tr("Ausfälle 30 Tage", "Outages 30 days")},
            "downtime_7d": {"name": tr("Ausfallzeit 7 Tage", "Downtime 7 days")},
            "availability_7d": {"name": tr("Verfügbarkeit 7 Tage", "Availability 7 days")},
            "availability_30d": {"name": tr("Verfügbarkeit 30 Tage", "Availability 30 days")},
            "last_outage": {"name": tr("Letzter Ausfall", "Last outage")},
            "last_outage_duration": {"name": tr("Dauer letzter Ausfall", "Last outage duration")},
            "last_check": {"name": tr("Letzte Überprüfung", "Last check")},
            "wan_ip": {"name": tr("WAN-IP", "WAN IP")},
            "last_reconnect": {"name": tr("Letzte Neueinwahl", "Last reconnect")},
            "reconnect_result": {"name": tr("Ergebnis Neueinwahl", "Reconnect result"), "state": {
                "ok_new_ip": tr("Erfolgreich, neue IP", "Success, new IP"), "ok_same_ip": tr("Erfolgreich, gleiche IP", "Success, same IP"),
                "no_effect": tr("Keine Wirkung", "No effect"), "error": tr("Fehler", "Error"),
                "triggered": tr("Ausgelöst", "Triggered")}},
        },
        "binary_sensor": {
            "internet": {"name": tr("Internet", "Internet")},
            "router": {"name": tr("Router", "Router")},
            "emergency": {"name": tr("Notbetrieb", "Backup operation")},
            "phone": {"name": tr("Notfall-Handy meldet sich", "Backup phone reporting")},
            "router_link": {"name": tr("Router-Anbindung gestört", "Router connection problem")},
        },
        "button": {
            "activate_dayflat": {"name": tr("Tagesflat freischalten", "Activate day pass")},
            "restrict": {"name": tr("Wieder einschränken", "Restrict again")},
            "reset_usage": {"name": tr("Verbrauch zurücksetzen", "Reset usage")},
            "reconnect_now": {"name": tr("Jetzt neu verbinden", "Reconnect now")},
            "test_notify": {"name": tr("Testmeldung senden", "Send test message")},
        },
        "switch": {"daily_reconnect": {"name": tr("Tägliche Neueinwahl", "Daily reconnect")}},
        "time": {"reconnect_time": {"name": tr("Uhrzeit Neueinwahl", "Reconnect time")}},
    }
    selector = {
        "router_type": {"options": {"unifi": "UniFi", "switches": tr("Schalter je Gerät (z. B. FRITZ!Box)", "Switch per device (e.g. FRITZ!Box)"),
                                    "scripts": tr("Eigene Skripte", "Custom scripts"), "none": tr("Keine Sperre, nur Überwachung", "No blocking, monitor only")}},
        "group": {"options": {"always": tr("Immer", "Always"), "dayflat": tr("Mit Tagesflat", "With day pass"), "never": tr("Nie", "Never")}},
        "group_inherit": {"options": {"always": tr("Immer", "Always"), "dayflat": tr("Mit Tagesflat", "With day pass"), "never": tr("Nie", "Never"), "inherit": tr("Erben", "Inherit")}},
        "method": {"options": {"pppd_hup": tr("SSH: PPPoE-Dienst neu verbinden (UniFi, empfohlen)", "SSH: restart PPPoE session (UniFi)"),
                               "ip_link": tr("SSH: Schnittstelle aus/an", "SSH: interface down/up"),
                               "ha_action": tr("HA-Button oder Skript (z. B. FRITZ!Box)", "HA button or script (e.g. FRITZ!Box)")}},
        "standby": {"options": {"warm": tr("Warm – Backup ständig verbunden, automatische Umschaltung", "Warm – always connected"),
                                "cold": tr("Kalt – Backup aus, im Ausfall von Hand einschalten", "Cold – off, switched on by hand")}},
        "detection": {"options": {"active_wan": tr("Aktive Leitung (z. B. UniFi Active WAN ID)", "Active line sensor"),
                                  "primary_off": tr("Status der Hauptleitung (Binärsensor)", "Main line status"),
                                  "custom": tr("Eigener Sensor", "Custom sensor"),
                                  "monitor": tr("Eigene Pings von HomeLines", "HomeLines’ own pings")}},
    }
    exceptions = {
        "not_in_emergency": {"message": tr("Freischalten geht nur im Notbetrieb.", "Only possible during backup operation.")},
        "booked_in_future": {"message": tr("Die Buchungszeit liegt in der Zukunft.", "Booking time is in the future.")},
        "flat_expired": {"message": tr("Diese Tagesflat ist schon abgelaufen.", "This day pass has already expired.")},
        "unknown_entry": {"message": tr("HomeLines ist nicht eingerichtet.", "HomeLines is not set up.")},
    }
    services = {
        "activate_dayflat": {"name": tr("Tagesflat freischalten", "Activate day pass"), "description": tr("Gibt die Gruppe „Mit Tagesflat“ frei.", "Allows group “With day pass”."),
                             "fields": {"entry_id": {"name": "HomeLines"}, "booked_at": {"name": tr("Gebucht um", "Booked at"), "description": tr("Ohne Angabe: jetzt.", "Default: now.")}}},
        "restrict": {"name": tr("Wieder einschränken", "Restrict again"), "description": tr("Zurück auf Notbetrieb.", "Back to backup operation."), "fields": {"entry_id": {"name": "HomeLines"}}},
        "set_group": {"name": tr("Gruppe setzen", "Set group"), "description": tr("Ordnet Geräte (MAC) oder Netze einer Gruppe zu.", "Assigns devices or networks to a group."),
                      "fields": {"entry_id": {"name": "HomeLines"}, "kind": {"name": tr("Art", "Kind")}, "targets": {"name": tr("Ziele", "Targets")}, "group": {"name": tr("Gruppe", "Group")}}},
        "reset_usage": {"name": tr("Verbrauch zurücksetzen", "Reset usage"), "description": tr("Setzt Verbrauch und Kosten auf null, z. B. nach dem Aufladen.", "Resets usage and costs."),
                        "fields": {"entry_id": {"name": "HomeLines"}, "start_balance": {"name": tr("Neues Guthaben", "New balance")}}},
        "test_notify": {"name": tr("Testmeldung senden", "Send test message"), "description": tr("Schickt eine Testmeldung an alle Empfänger.", "Sends a test message to all recipients."), "fields": {"entry_id": {"name": "HomeLines"}}},
        "reconnect": {"name": tr("Neu verbinden", "Reconnect"), "description": tr("Löst sofort eine PPPoE-Neueinwahl aus.", "Triggers a PPPoE reconnect now."), "fields": {"entry_id": {"name": "HomeLines"}}},
    }
    issues = {
        "legacy_running": {"title": tr("LineGuard läuft noch", "LineGuard is still running"),
                           "description": tr("HomeLines hat die Einrichtung von LineGuard übernommen. Entferne jetzt LineGuard unter Einstellungen → Geräte & Dienste und lösche den Ordner custom_components/lineguard (bzw. deinstalliere LineGuard). HomeLines räumt danach die alte Regel im Router auf.",
                                             "HomeLines has taken over the LineGuard setup. Remove LineGuard under Settings → Devices & services and delete custom_components/lineguard. HomeLines then removes the old router rule.")},
        "primary_wan_missing": {"title": tr("Hauptleitung im Router nicht gefunden", "Primary line not found on router"),
                                "description": tr("Die Leitung „{name}“ für die Sperrregel gibt es in UniFi nicht mehr, vermutlich wurde sie neu angelegt. HomeLines konnte sie auch über Name und WAN-Gruppe nicht zuordnen. Wähle sie unter HomeLines → Konfigurieren → Leitungen → „Hauptleitung für die Sperrregel“ neu aus.",
                                                  "The line “{name}” used for the block rule no longer exists in UniFi. Choose it again under HomeLines → Configure → Lines.")},
    }
    return {
        "config": {"step": steps, "error": errors, "abort": {"already_configured": tr("Dieser Router ist schon eingerichtet.", "Already configured.")}},
        "options": {"step": opt_steps, "error": errors},
        "entity": entity, "selector": selector, "exceptions": exceptions, "services": services, "issues": issues,
    }


(ROOT / "strings.json").write_text(json.dumps(build("en"), ensure_ascii=False, indent=2))
(ROOT / "translations" / "en.json").write_text(json.dumps(build("en"), ensure_ascii=False, indent=2))
(ROOT / "translations" / "de.json").write_text(json.dumps(build("de"), ensure_ascii=False, indent=2))
print("ok")
