/* HomeLines-Karte – Internet Monitor & Mobile Failover */
const HL_VERSION = "0.9.0";
// Haus-Symbol aus dem HomeLines-Logo (brand/icon.png), für den Kartenkopf
/* Logo mit Schriftzug (ab 0.9.0): Schrift in currentColor, passt zu hell und dunkel */
const HL_WORD = `<svg class="hlword" viewBox="14 22 2400 742" role="img" aria-label="HomeLines"><path fill="#bc001b" d="M777.09,701.32l-4.58-320.59,159.85,2.4L476.11,27.59,19.86,383.13l131.46,3.42,5.88,315.74L777.09,701.32ZM469.2,409.08h-92.66v-92.66h92.66V409.08ZM469.2,302.61h-92.66v-92.64h92.66V302.61ZM575.67,409.08h-92.65v-92.66h92.65V409.08ZM575.67,302.61h-92.65v-92.64h92.65V302.61Z"/><path fill="#d60029" fill-rule="evenodd" d="M607.62,753.58c-7.32,0-13.27-5.95-13.27-13.27v-134.14c0-7.32,5.95-13.27,13.27-13.27s13.26,5.95,13.28,13.26v134.15C620.89,747.63,614.94,753.58,607.62,753.58Z"/><path fill="#fff" d="M607.62,598.57c4.18,0,7.6,3.42,7.61,7.6v134.14c-.01,4.18-3.43,7.6-7.61,7.6s-7.6-3.42-7.6-7.6v-134.14C600.02,601.99,603.43,598.57,607.62,598.57H607.62ZM607.62,587.23c-10.45,0-18.94,8.5-18.94,18.94v134.14c0,10.44,8.49,18.94,18.94,18.94s18.94-8.5,18.94-18.94v-134.14C626.55,595.72,618.05,587.23,607.62,587.23H607.62Z"/><path fill="#7f0119" fill-rule="evenodd" d="M665.25,753.58c-7.32,0-13.27-5.95-13.27-13.27v-194.14c0-7.32,5.95-13.27,13.27-13.27s13.26,5.95,13.28,13.26v194.15C678.52,747.63,672.57,753.58,665.25,753.58Z"/><path fill="#fff" d="M665.25,538.57c4.18,0,7.6,3.42,7.61,7.6v194.14c-.01,4.18-3.43,7.6-7.61,7.6s-7.6-3.42-7.6-7.6v-194.14C657.65,541.99,661.06,538.57,665.25,538.57H665.25ZM665.25,527.23c-10.45,0-18.94,8.5-18.94,18.94v194.14c0,10.44,8.49,18.94,18.94,18.94s18.94-8.5,18.94-18.94v-194.14C684.17,535.72,675.67,527.23,665.25,527.23H665.25Z"/><path fill="#d67c8e" fill-rule="evenodd" d="M724.16,753.58c-7.31,0-13.27-5.95-13.27-13.27v-164.14c0-7.32,5.96-13.27,13.27-13.27s13.27,5.95,13.28,13.26v164.15C737.43,747.63,731.48,753.58,724.16,753.58Z"/><path fill="#fff" d="M724.16,568.57c4.19,0,7.6,3.42,7.61,7.6v164.14c0,4.18-3.42,7.6-7.61,7.6s-7.6-3.42-7.6-7.6v-164.14C716.56,571.99,719.98,568.57,724.16,568.57H724.16ZM724.16,557.23c-10.44,0-18.94,8.5-18.94,18.94v164.14c0,10.44,8.5,18.94,18.94,18.94s18.94-8.5,18.94-18.94v-164.14C743.09,565.72,734.59,557.23,724.16,557.23H724.16Z"/><g fill="currentColor"><path d="M859.31,442.82v108.35h135.71v-108.35h17.51v245.88h-17.51v-122.94h-135.71v122.94h-17.51v-245.88H859.31Z"/><path d="M1114.31,692.71c-45.24,0-80.26-35.38-80.26-90.1,0-59.83,39.4-93.03,82.81-93.03,48.52,0,81.35,36.48,81.35,90.11,0,64.94-44.87,93.02-83.54,93.02H1114.31ZM1115.4,678.12c36.48,0,65.3-32.83,65.3-77.7,0-32.1-17.87-76.25-64.2-76.25s-64.94,39.77-64.94,77.34c0,43.78,27.73,76.61,63.48,76.61H1115.4Z"/><path d="M1218.65,555.55c0-16.05-.37-28.09-1.46-41.96h16.41l1.1,30.65h.73c11.31-20.07,28.09-34.66,56.91-34.66,24.07,0,42.68,16.05,50.34,37.94h.73c4.74-10.21,11.31-18.24,17.88-23.71,11.3-9.12,22.98-14.23,41.58-14.23,17.15,0,57.28,9.49,57.28,75.88v103.24h-17.51v-101.78c0-39.4-15.32-62.75-45.6-62.75-21.89,0-39.04,16.42-45.97,34.66-1.46,5.11-2.92,10.95-2.92,17.51v112.36h-17.51v-109.8c0-31.38-14.96-54.73-43.41-54.73-23.35,0-41.95,18.97-48.52,39.4-1.46,5.11-2.55,10.95-2.55,17.15v107.98h-17.51V555.55Z"/><path d="M1496.99,599.32c0,55.82,30.65,78.07,66.76,78.07,25.54,0,38.67-5.1,48.52-9.85l4.38,13.5c-6.57,3.65-24.44,11.31-55.09,11.31-50.34,0-81.71-36.48-81.71-87.92,0-58.37,33.56-94.85,78.8-94.85,57.27,0,68.21,53.99,68.21,79.17,0,4.74,0,7.29-.73,10.57H1496.99ZM1608.62,585.46c.37-24.44-9.85-61.29-52.16-61.29-38.67,0-55.09,34.3-58.37,61.29H1608.62Z"/><path d="M1659.51,442.82h44.87v208.31h101.06v37.57h-145.93V442.82Z"/><path d="M1850.34,485.5c-14.95,0-24.8-10.94-24.8-24.07,0-13.87,10.21-24.44,25.17-24.44s24.81,10.57,25.17,24.44c0,13.13-9.85,24.07-25.17,24.07H1850.34ZM1828.09,688.7v-177.66h44.87v177.66H1828.09Z"/><path d="M1912.69,563.94c0-20.43-.73-37.58-1.46-52.9h39.04l2.18,26.63h1.1c8.02-13.86,27.36-30.64,56.91-30.64,31.01,0,63.11,20.06,63.11,76.24v105.43h-44.87v-100.32c0-25.54-9.49-44.87-33.93-44.87-17.87,0-30.28,12.77-35.02,26.27-1.46,3.64-2.19,9.12-2.19,14.22v104.7h-44.87V563.94Z"/><path d="M2145.11,612.46c1.09,32.1,26.27,45.96,54.72,45.96,20.8,0,35.39-3.28,49.25-8.02l6.57,30.64c-15.33,6.57-36.48,11.31-62.02,11.31-57.64,0-91.57-35.39-91.57-89.74,0-49.25,29.92-95.58,86.83-95.58s76.61,47.42,76.61,86.46c0,8.39-.73,14.95-1.46,18.97H2145.11ZM2223.18,581.08c.36-16.41-6.93-43.41-36.85-43.41-27.72,0-39.4,25.17-41.22,43.41H2223.18Z"/><path d="M2291.29,647.11c9.85,6.21,29.18,13.14,45.23,13.14,19.7,0,28.46-8.39,28.46-20.07s-7.3-17.87-29.19-25.9c-34.65-11.67-48.88-30.64-48.88-51.8,0-31.37,25.9-55.45,67.12-55.45,19.7,0,36.85,4.74,47.43,10.58l-9.12,31.37c-7.3-4.38-21.89-10.21-37.58-10.21s-24.8,8.02-24.8,18.97,8.39,16.41,31.01,24.8c32.46,11.31,47.06,27.73,47.42,54,0,32.46-25.17,55.81-72.23,55.81-21.52,0-40.86-5.11-53.99-12.4L2291.29,647.11Z"/></g></svg>`;
const HL_LOGO = `<svg class="hllogo" viewBox="14 22 924 742" aria-hidden="true"><path fill="#bc001b" d="M777.09,701.32l-4.58-320.59,159.85,2.4L476.11,27.59,19.86,383.13l131.46,3.42,5.88,315.74L777.09,701.32ZM469.2,409.08h-92.66v-92.66h92.66V409.08ZM469.2,302.61h-92.66v-92.64h92.66V302.61ZM575.67,409.08h-92.65v-92.66h92.65V409.08ZM575.67,302.61h-92.65v-92.64h92.65V302.61Z"/><path fill="#d60029" fill-rule="evenodd" d="M607.62,753.58c-7.32,0-13.27-5.95-13.27-13.27v-134.14c0-7.32,5.95-13.27,13.27-13.27s13.26,5.95,13.28,13.26v134.15C620.89,747.63,614.94,753.58,607.62,753.58Z"/><path fill="#fff" d="M607.62,598.57c4.18,0,7.6,3.42,7.61,7.6v134.14c-.01,4.18-3.43,7.6-7.61,7.6s-7.6-3.42-7.6-7.6v-134.14C600.02,601.99,603.43,598.57,607.62,598.57H607.62ZM607.62,587.23c-10.45,0-18.94,8.5-18.94,18.94v134.14c0,10.44,8.49,18.94,18.94,18.94s18.94-8.5,18.94-18.94v-134.14C626.55,595.72,618.05,587.23,607.62,587.23H607.62Z"/><path fill="#7f0119" fill-rule="evenodd" d="M665.25,753.58c-7.32,0-13.27-5.95-13.27-13.27v-194.14c0-7.32,5.95-13.27,13.27-13.27s13.26,5.95,13.28,13.26v194.15C678.52,747.63,672.57,753.58,665.25,753.58Z"/><path fill="#fff" d="M665.25,538.57c4.18,0,7.6,3.42,7.61,7.6v194.14c-.01,4.18-3.43,7.6-7.61,7.6s-7.6-3.42-7.6-7.6v-194.14C657.65,541.99,661.06,538.57,665.25,538.57H665.25ZM665.25,527.23c-10.45,0-18.94,8.5-18.94,18.94v194.14c0,10.44,8.49,18.94,18.94,18.94s18.94-8.5,18.94-18.94v-194.14C684.17,535.72,675.67,527.23,665.25,527.23H665.25Z"/><path fill="#d67c8e" fill-rule="evenodd" d="M724.16,753.58c-7.31,0-13.27-5.95-13.27-13.27v-164.14c0-7.32,5.96-13.27,13.27-13.27s13.27,5.95,13.28,13.26v164.15C737.43,747.63,731.48,753.58,724.16,753.58Z"/><path fill="#fff" d="M724.16,568.57c4.19,0,7.6,3.42,7.61,7.6v164.14c0,4.18-3.42,7.6-7.61,7.6s-7.6-3.42-7.6-7.6v-164.14C716.56,571.99,719.98,568.57,724.16,568.57H724.16ZM724.16,557.23c-10.44,0-18.94,8.5-18.94,18.94v164.14c0,10.44,8.5,18.94,18.94,18.94s18.94-8.5,18.94-18.94v-164.14C743.09,565.72,734.59,557.23,724.16,557.23H724.16Z"/></svg>`;

const T = {
  de: {
    normal: "Normalbetrieb", emergency: "Notbetrieb", dayflat: "Tagesflat aktiv",
    always: "Immer", dayflat_g: "Mit Tagesflat", never: "Nie", inherit: "Erben",
    allMain: "Alles läuft über die Hauptleitung", since: "seit", via: "über",
    hintEmergency: "Nur die Gruppe Immer ist online. Buche die Tagesflat und gib dann frei.",
    plannedHint: "Geplante Neueinwahl läuft – der kurze Wechsel auf Mobilfunk ist beabsichtigt.",
    back: "Zurück auf Notbetrieb in", flatUntil: "Tagesflat bis", restoreAt: "Rückschaltung", orMain: "oder sobald die Hauptleitung zurück ist",
    unlock: "Tagesflat freischalten", restrict: "Wieder einschränken", book: "Tagesflat buchen", devices: "Geräte",
    online: "Online", since_reset: "Seit Reset", cost: "Kosten", balance: "Guthaben ca.",
    checklist: "Notfall-Kette", phoneReports: "Handy meldet sich", phoneSilent: "Handy meldet sich nicht",
    ago: "vor", min: "min", mobile: "Mobilfunk", dataOff: "Mobile Daten aus", usb: "USB-Kabel zum Router steckt",
    noUsb: "Kein USB-Kabel erkannt", backupOnline: "Backup-Leitung online", backupOffline: "Backup-Leitung offline",
    flatOn: "Tagesflat aktiv", flatOff: "Tagesflat nicht aktiv", perMb: "ct/MB",
    monitor: "Internet-Überwachung", avail: "Verfügbarkeit 7 T", outages: "Ausfälle 24 h / 7 T", latency: "Latenz",
    lastOutage: "Letzter Ausfall", none: "keiner", reconnect: "Neueinwahl", next: "täglich", reconnectNow: "Jetzt neu verbinden",
    last: "zuletzt",
    confirmTitle: "Tagesflat wirklich gebucht?", confirmBody: "Danach dürfen alle Geräte außer der Gruppe Nie über Mobilfunk. Der Timer läuft ab dem Buchungszeitpunkt.",
    bookedAt: "Gebucht um", iBooked: "Ich habe die Tagesflat gebucht", cancel: "Abbrechen", confirm: "Freischalten",
    restrictTitle: "Wieder einschränken?", restrictBody: "Danach ist nur noch die Gruppe Immer über Mobilfunk online. Der Timer wird beendet.",
    errConfirm: "Bestätige zuerst die Buchung.", errTime: "Trag ein, wann du gebucht hast.",
    errors: { not_in_emergency: "Freischalten geht nur im Notbetrieb.", booked_in_future: "Die Buchungszeit liegt in der Zukunft.", flat_expired: "Diese Tagesflat ist schon abgelaufen. Buche eine neue." },
    flatEnds: "Tagesflat endet", today: "heute", tomorrow: "morgen", yesterday: "gestern",
    devTitle: "Geräte bei Mobilfunk", search: "Gerät suchen", networks: "Netze", deviceList: "Geräte",
    allGroups: "Alle", fromNet: "vom Netz", fromDefault: "Standard", newDevices: "Neue Geräte landen in", done: "Fertig",
    noDevices: "Kein Gerät gefunden.", refresh: "Neu laden", reset: "Zurücksetzen", resetTitle: "Verbrauch zurücksetzen?",
    resetBody: "Verbrauch und Kosten starten wieder bei null. Trag dein aktuelles Guthaben ein, etwa nach dem Aufladen.", newBalance: "Aktuelles Guthaben",
    worthIt: "Ab hier lohnt sich die Tagesflat", routerError: "Router-Anbindung gestört", openOptions: "Optionen öffnen",
    details: "Details", speed: "Geschwindigkeit",
    netMissing: "Netz nicht mehr gefunden – wird nicht an den Router geschickt", remove: "Entfernen", notSetUp: "HomeLines antwortet noch nicht – ist die Integration eingerichtet? Ich versuche es weiter …",
    connecting: "Verbinde mit HomeLines …", reconnecting: "Verbindung zu Home Assistant unterbrochen – Daten von",
    lineStates: { online: "online", offline: "offline", unavailable: "nicht erreichbar", unknown: "unbekannt" }, active: "aktiv", backup: "Backup",
    coldStandby: "Backup in kalter Bereitschaft", assistTitle: "Notfall-Internet einschalten", returnTitle: "Notfall-Handy zurückstellen",
    returnHint: "Die Hauptleitung ist zurück. Damit nicht weiter Daten über die SIM laufen:", doneLink: "Erledigt",
    notConnected: "nicht angeschlossen", reserve: "Reserve", phoneReady: "Handy bereit",
    pending: "Hauptleitung antwortet nicht – wird bestätigt in", seconds: "s", unchecked: "nicht prüfbar",
    steps: { book: "Tagesflat buchen und hier freischalten", wifi_off: "WLAN am Notfall-Handy aus", data_on: "Mobile Daten an",
      usb: "USB-Kabel zum Notfall-Router steckt", tether: "USB-Tethering an – Backup-Leitung online",
      tether_off: "USB-Tethering aus", data_off: "Mobile Daten aus", wifi_on: "WLAN wieder an" },
    results: { ok_new_ip: "erfolgreich, neue IP", ok_same_ip: "erfolgreich, gleiche IP", no_effect: "keine Wirkung", error: "Fehler", triggered: "ausgelöst" },
  },
};
const tr = T.de;

const css = `
:host{--hl-ok:var(--success-color,#2e7d32);--hl-warn:var(--warning-color,#f29d0b);--hl-err:var(--error-color,#db4437);--hl-acc:var(--primary-color,#03a9f4)}
ha-card{padding:16px;overflow:hidden;position:relative}
*{box-sizing:border-box}
.hd{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}
.hd .t{display:flex;align-items:center;gap:10px;min-width:0}
.hd ha-icon{color:var(--secondary-text-color)}
.ttl{font-size:16px;font-weight:500;margin:0}
.sub{font-size:13px;color:var(--secondary-text-color);margin:0}
.badge{font-size:12px;padding:3px 10px;border-radius:8px;white-space:nowrap}
.ok{background:color-mix(in srgb,var(--hl-ok) 16%,transparent);color:var(--hl-ok)}
.warn{background:color-mix(in srgb,var(--hl-warn) 18%,transparent);color:color-mix(in srgb,var(--hl-warn) 70%,var(--primary-text-color))}
.err{background:color-mix(in srgb,var(--hl-err) 14%,transparent);color:var(--hl-err)}
.mut{background:color-mix(in srgb,var(--secondary-text-color) 10%,transparent);color:var(--secondary-text-color)}
.wans{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0;padding-bottom:12px;border-bottom:1px solid var(--divider-color)}
.wan{display:inline-flex;align-items:center;gap:6px;font-size:12px;padding:4px 10px;border-radius:8px}
.wan b{font-weight:500}
.hllogo{width:34px;height:28px;flex:none}
.hlword{height:44px;width:auto;flex:none;display:block;color:var(--primary-text-color)}
.lines{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;margin:12px 0}
.line{position:relative;border-radius:12px;padding:10px 12px;border:1px solid var(--divider-color);background:var(--card-background-color,transparent);min-width:0}
.line[data-nav]{cursor:pointer}.line[data-nav]:hover{border-color:var(--secondary-text-color)}
.line .id{font-size:11px;color:var(--secondary-text-color)}
.line b{display:block;font-size:15px;font-weight:500;margin:1px 0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.line .st{font-size:12px;color:var(--secondary-text-color)}
.line .inf{font-size:13px;margin-top:6px;font-variant-numeric:tabular-nums}
.line.act{border:2px solid var(--hl-ok);background:color-mix(in srgb,var(--hl-ok) 10%,transparent)}
.line.act b,.line.act .inf{color:var(--hl-ok)}
.line.off{border-color:var(--hl-err)}.line.off .st{color:var(--hl-err)}
.line.na{opacity:.6;border-style:dashed}
.line .tag{position:absolute;top:8px;right:10px;font-size:11px;padding:1px 7px;border-radius:8px;color:var(--hl-ok);border:1px solid var(--hl-ok)}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0 2px}
.hlovw{display:grid;grid-template-columns:repeat(auto-fill,minmax(max(220px,calc(50% - 4px)),1fr));gap:8px;margin:12px 0 4px}
.hlov{display:flex;align-items:center;gap:12px;padding:10px 12px;border:1px solid var(--divider-color);border-radius:12px;cursor:pointer;min-width:0}
.hlov .hlov-i{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none;background:color-mix(in srgb,var(--secondary-text-color) 12%,transparent);color:var(--secondary-text-color)}
.hlov .hlov-t{min-width:0;flex:1}.hlov .hlov-n{font-weight:500;font-size:14px}.hlov .hlov-s{font-size:13px;color:var(--secondary-text-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hlov.warn{border-color:var(--hl-warn);background:color-mix(in srgb,var(--hl-warn) 10%,transparent)}.hlov.warn .hlov-i{color:var(--hl-warn);background:color-mix(in srgb,var(--hl-warn) 18%,transparent)}.hlov.warn .hlov-s{color:var(--hl-warn)}
.hlov.err{border-color:var(--hl-err);background:color-mix(in srgb,var(--hl-err) 8%,transparent)}.hlov.err .hlov-i{color:var(--hl-err);background:color-mix(in srgb,var(--hl-err) 16%,transparent)}.hlov.err .hlov-s{color:var(--hl-err)}
.hlovx{min-width:0;display:block}.hlovx>*{display:block;height:100%}
.hlov .hlov-c{color:var(--secondary-text-color);--mdc-icon-size:20px}
.chip{font-size:12px;padding:3px 9px;border-radius:8px;border:1px solid var(--divider-color);color:var(--secondary-text-color)}
.dot{width:8px;height:8px;border-radius:50%;background:currentColor;display:inline-block}
.box{border-radius:8px;padding:10px 12px;font-size:13px;margin-bottom:12px;line-height:1.5}
.timer .row1{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.cd{font-size:24px;font-weight:500;font-variant-numeric:tabular-nums}
.bar{height:6px;border-radius:3px;background:color-mix(in srgb,var(--hl-ok) 20%,transparent);margin-top:8px;overflow:hidden}
.bar>div{height:6px;background:var(--hl-ok)}
.btns{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.b{cursor:pointer;user-select:none;border:1px solid var(--divider-color);border-radius:8px;padding:7px 12px;font-size:14px;display:inline-flex;align-items:center;gap:6px;background:none;color:var(--primary-text-color);font-family:inherit;text-decoration:none}
.b:hover{background:color-mix(in srgb,var(--primary-text-color) 5%,transparent)}
.b ha-icon{--mdc-icon-size:18px}
.bp{background:var(--hl-acc);color:var(--text-primary-color,#fff);border-color:transparent}
.bp:hover{background:color-mix(in srgb,var(--hl-acc) 88%,#000)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin-bottom:14px}
.m{background:color-mix(in srgb,var(--primary-text-color) 4%,transparent);border-radius:8px;padding:9px 11px}
.ml{font-size:12px;color:var(--secondary-text-color);margin:0}
.mv{font-size:19px;font-weight:500;margin:2px 0 0;font-variant-numeric:tabular-nums}
.sec{font-size:13px;color:var(--secondary-text-color);margin:4px 0 2px;display:flex;justify-content:space-between;align-items:center}
.row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:7px 0;border-top:1px solid var(--divider-color);font-size:14px;flex-wrap:wrap}
.row .r{color:var(--secondary-text-color);font-size:13px}
.row ha-icon{--mdc-icon-size:18px;margin-right:4px;vertical-align:-3px}
.ver{font-size:10px;color:var(--secondary-text-color);text-align:right;opacity:.6;margin-top:6px}
.i-ok{color:var(--hl-ok)}.i-err{color:var(--hl-err)}.i-warn{color:var(--hl-warn)}.i-mut{color:var(--secondary-text-color)}
.link{cursor:pointer;color:var(--hl-acc);font-size:13px}
.ov{position:absolute;inset:0;background:rgba(0,0,0,.45);display:flex;align-items:flex-start;justify-content:center;padding:24px 8px;z-index:5;overflow:auto}
.dlg{background:var(--card-background-color,var(--ha-card-background,#fff));border-radius:12px;padding:16px;width:min(560px,100%);box-shadow:0 8px 24px rgba(0,0,0,.25)}
.dlg h3{margin:0 0 8px;font-size:16px;font-weight:500}
.dlg p{margin:0 0 12px;font-size:14px;color:var(--secondary-text-color);line-height:1.6}
.dlg .acts{display:flex;gap:8px;justify-content:flex-end;margin-top:14px}
.fld{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px;font-size:14px}
input[type=time],input[type=number],input[type=search]{font:inherit;padding:6px 8px;border-radius:8px;border:1px solid var(--divider-color);background:var(--card-background-color);color:var(--primary-text-color)}
input[type=search]{width:100%}
.chk{display:flex;gap:8px;align-items:center;font-size:14px;margin:8px 0;cursor:pointer}
.e{font-size:13px;color:var(--hl-err);margin:4px 0}
.pv{font-size:12px;color:var(--secondary-text-color);margin:0 0 8px}
.seg{display:inline-flex;flex-wrap:nowrap}
.chip{cursor:pointer;user-select:none;font-size:12px;padding:4px 9px;border:1px solid var(--divider-color);margin-left:-1px;color:var(--secondary-text-color);white-space:nowrap}
.chip:first-child{border-radius:8px 0 0 8px;margin-left:0}.chip:last-child{border-radius:0 8px 8px 0}
.chip.on{background:color-mix(in srgb,var(--hl-acc) 16%,transparent);color:var(--hl-acc);border-color:color-mix(in srgb,var(--hl-acc) 50%,transparent);position:relative}
.chip.inh{background:color-mix(in srgb,var(--hl-acc) 7%,transparent);color:var(--hl-acc);border-style:dashed}
.tabs{display:flex;gap:6px;margin:8px 0}
.tab{cursor:pointer;font-size:13px;padding:4px 10px;border-radius:8px;color:var(--secondary-text-color)}
.tab.on{background:color-mix(in srgb,var(--hl-acc) 14%,transparent);color:var(--hl-acc)}
.dn{display:flex;flex-direction:column;min-width:0}
.dn small{font-size:11px;color:var(--secondary-text-color)}
.list{max-height:420px;overflow:auto}
.steps{margin:6px 0 0;padding:0;list-style:none}
.steps li{display:flex;align-items:center;gap:8px;padding:5px 0;font-size:14px;color:var(--primary-text-color)}
.steps .n{width:22px;height:22px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0;border:1px solid currentColor}
.steps .d{background:var(--hl-ok);color:#fff;border-color:var(--hl-ok)}
.steps .x{color:var(--hl-warn)}.steps .u{color:var(--secondary-text-color);border-style:dashed}
.steps small{color:var(--secondary-text-color);font-size:12px}
`;

function esc(s) { return String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function hlHead(title, sub) {
  // Standardtitel: Logo mit Schriftzug; eigener Titel: Haus + Titel
  return title === "HomeLines" ? `<div>${HL_WORD}<p class="sub">${sub}</p></div>`
    : `${HL_LOGO}<div><p class="ttl">${esc(title)}</p><p class="sub">${sub}</p></div>`;
}
/* Zahl mit Einheit (ab 0.9.0): Euro immer mit zwei Nachkommastellen */
function hlNum(v, u, decimals) {
  const money = /^(€|EUR)$/i.test(u || "");
  const d = money ? 2 : decimals ?? (Math.abs(v) >= 100 ? 0 : 1);
  return `${v.toLocaleString("de-DE", { minimumFractionDigits: money ? 2 : 0, maximumFractionDigits: d })}${u ? " " + u : ""}`;
}
function eur(v) { return (Number(v) || 0).toLocaleString("de-DE", { style: "currency", currency: "EUR" }); }
function p2(n) { return String(n).padStart(2, "0"); }
function hm(d) { return `${p2(d.getHours())}:${p2(d.getMinutes())}`; }
function dayword(d) {
  const n = new Date(); const a = new Date(d.getFullYear(), d.getMonth(), d.getDate()); const b = new Date(n.getFullYear(), n.getMonth(), n.getDate());
  const diff = Math.round((a - b) / 86400000);
  return diff === 0 ? tr.today : diff === 1 ? tr.tomorrow : diff === -1 ? tr.yesterday : d.toLocaleDateString("de-DE");
}
function when(iso) { if (!iso) return "–"; const d = new Date(iso); return `${dayword(d)} ${hm(d)}`; }
function agoMin(iso) { return iso ? Math.max(0, Math.round((Date.now() - new Date(iso)) / 60000)) : null; }
function dur(s) { s = Math.round(s || 0); const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60); return h ? `${h} h ${m} min` : m ? `${m} min` : `${s} s`; }
function mb(v) { v = Number(v) || 0; return v >= 1024 ? `${(v / 1024).toLocaleString("de-DE", { maximumFractionDigits: 2 })} GB` : `${v.toLocaleString("de-DE", { maximumFractionDigits: 1 })} MB`; }
const GROUPS = ["always", "dayflat", "never"];
const gname = g => g === "dayflat" ? tr.dayflat_g : tr[g];

/* Gemeinsame, selbstheilende Datenleitung: ein Abo je Eintrag für alle Karten.
   Nach einem HA-Neustart ist HomeLines oft noch nicht geladen – dann alle paar Sekunden neu versuchen. */
class HLFeed {
  constructor(conn, entryId) {
    this.conn = conn; this.entryId = entryId || ""; this.ls = new Set();
    this.data = null; this.state = "connecting"; this.tries = 0; this.at = null;
    this._ready = () => { this.unsub = null; this.tries = 0; this._start(); };
    this._disc = () => { this.unsub = null; clearTimeout(this.timer); this.state = "offline"; this._emit(); };
    conn.addEventListener("ready", this._ready);
    conn.addEventListener("disconnected", this._disc);
    this._start();
  }
  _start() {
    clearTimeout(this.timer);
    if (this.closed) return;
    const msg = { type: "homelines/subscribe" };
    if (this.entryId) msg.entry_id = this.entryId;
    const gen = this.gen = (this.gen || 0) + 1;
    this.conn.subscribeMessage(d => {
      if (gen !== this.gen) return;
      this.data = d; this.state = "ok"; this.tries = 0; this.at = Date.now(); this._emit();
    }, msg, { resubscribe: false }).then(u => {
      if (this.closed || gen !== this.gen) { try { u(); } catch (e) {} return; }
      this.unsub = u;
    }).catch(() => {
      if (this.closed || gen !== this.gen) return;
      this.tries++;
      this.state = this.tries > 6 ? "missing" : "connecting";
      this._emit();
      this.timer = setTimeout(() => this._start(), this.tries > 6 ? 15000 : 4000);
    });
  }
  add(fn) { clearTimeout(this.closeTimer); this.ls.add(fn); fn(this); }
  remove(fn) {
    this.ls.delete(fn);
    if (!this.ls.size) this.closeTimer = setTimeout(() => this.close(), 15000);
  }
  close() {
    this.closed = true; clearTimeout(this.timer);
    this.conn.removeEventListener("ready", this._ready);
    this.conn.removeEventListener("disconnected", this._disc);
    if (this.unsub) { try { this.unsub().catch?.(() => {}); } catch (e) {} }
    HL_FEEDS.delete(this.key);
  }
  _emit() { this.ls.forEach(fn => { try { fn(this); } catch (e) { console.error(e); } }); }
}
const HL_FEEDS = window.__hlFeeds || (window.__hlFeeds = new Map());
function hlFeed(hass, entryId) {
  const key = entryId || "";
  let f = HL_FEEDS.get(key);
  if (f && f.conn !== hass.connection) { f.close(); f = null; }
  if (!f) { f = new HLFeed(hass.connection, entryId); f.key = key; HL_FEEDS.set(key, f); }
  return f;
}
function hlStatusBox(f) {
  if (f.state === "missing") return `<div class="box warn">${tr.notSetUp}</div>`;
  return `<div class="box mut">${tr.connecting}</div>`;
}

class HomeLinesCard extends HTMLElement {
  setConfig(config) { this._config = config || {}; this._infos = {}; this._unsubInfos(); this._tileEls = []; }
  static getStubConfig() { return {}; }

  _unsubInfos() {
    (this._infoSubs || []).forEach(p => p.then(u => u && u()).catch(() => {}));
    this._infoSubs = [];
  }

  _subscribeInfos() {
    const lines = this._config.lines || {};
    this._unsubInfos();
    Object.entries(lines).forEach(([id, cfg]) => {
      if (!cfg || !cfg.info) return;
      this._infoSubs.push(this._hass.connection.subscribeMessage(r => {
        if (r && "result" in r) { this._infos[id] = String(r.result); this._render(); }
      }, { type: "render_template", template: String(cfg.info) }));
    });
  }
  getCardSize() { return 8; }

  set hass(hass) {
    this._hass = hass;
    if (this._detail && this._detail.open) this._detail.setHass(hass);
    (this._tileEls || []).forEach(t => { if (t) t.hass = hass; });
    if (this._s && this._main && this._config.overview !== false) {
      const key = hlOverviewEntities(this._s).map(e => hass.states[e] && hass.states[e].state).join("|");
      if (key !== this._ovKey) { this._ovKey = key; this._render(); }
    }
    if (!this._root) this._build();
    if (!this._feed && this.isConnected) this._subscribe();
    if (!this._infoSubs || !this._infoSubs.length) this._subscribeInfos();
  }

  connectedCallback() {
    if (this._hass && !this._feed) this._subscribe();
    if (this._hass && (!this._infoSubs || !this._infoSubs.length)) this._subscribeInfos();
    if (!this._tick) this._tick = setInterval(() => this._updateTimer(), 1000);
  }

  disconnectedCallback() {
    if (this._feed) { this._feed.remove(this._onFeed); this._feed = null; }
    this._unsubInfos();
    clearInterval(this._tick); this._tick = null;
  }

  _build() {
    this._root = this.attachShadow({ mode: "open" });
    this._root.innerHTML = `<style>${css}</style><ha-card><div id="main"></div><div class="ver">HomeLines ${HL_VERSION}</div><div id="dlg"></div></ha-card>`;
    this._main = this._root.getElementById("main");
    this._dlg = this._root.getElementById("dlg");
    this._root.addEventListener("click", e => this._onClick(e));
    this._root.addEventListener("input", e => this._onInput(e));
    this._view = { dialog: null, tab: "devices", filter: "all", q: "" };
    this._main.innerHTML = `<div class="box mut">${tr.connecting}</div>`;
  }

  _subscribe() {
    this._onFeed = this._onFeed || (f => {
      this._fstate = f.state;
      if (f.data) { this._s = f.data; this._render(); if (this._detailEl && this._detail && this._detail.open) this._detailEl.state = f.data; }
      else if (this._main) this._main.innerHTML = hlStatusBox(f);
    });
    this._feed = hlFeed(this._hass, this._config.entry_id);
    this._feed.add(this._onFeed);
  }

  _ws(type, extra = {}) {
    const msg = { type, ...extra };
    if (this._s) msg.entry_id = this._s.entry_id;
    return this._hass.connection.sendMessagePromise(msg);
  }

  /* ----------------------------------------------------------- Hauptansicht */
  _render() {
    const s = this._s; if (!s) return;
    const mode = s.mode;
    const badgeCls = mode === "normal" ? "ok" : mode === "dayflat" ? "ok" : "warn";
    const active = (s.wans || []).find(w => w.active);
    const sub = mode === "normal" ? `${tr.allMain}${active ? " · " + esc(active.name) : ""}`
      : `${tr.emergency} ${tr.since} ${when(s.since)} · ${tr.via} ${esc(active ? active.name : s.backup_wan)}`;
    const title = this._config.title || s.title || "HomeLines";

    const lcfg = this._config.lines || {};
    const ph0 = s.phone || {};
    const wans = (s.wans || []).filter(w => !(lcfg[w.id] && lcfg[w.id].hide)).map(w => {
      const cfg = lcfg[w.id] || {};
      const isAct = w.active || (w.backup && mode !== "normal" && w.state === "online");
      const cold = w.backup && s.standby === "cold" && mode === "normal" && w.state !== "online";
      const cls = isAct ? "act" : cold ? "" : w.state === "offline" ? (w.backup && mode === "normal" ? "" : "off")
        : (w.state === "unknown" && !w.entity_id && !cfg.info) ? "na" : "";
      let label = cold ? tr.coldStandby : (tr.lineStates[w.state] || w.state);
      if (cls === "na") label = cfg.na_text || tr.notConnected;
      if (!isAct && !w.backup && w.state === "online" && mode === "normal") label = `${tr.reserve} · ${label}`;
      let info = this._infos[w.id] || "";
      if (!info && !w.backup) {
        const ents = (((s.details || {}).lines || {})[w.id] || {}).entities || [];
        const nums = ents.map(e => this._hass.states[e]).filter(st => st && !isNaN(parseFloat(st.state)) && /^-?[\d.]+$/.test(st.state));
        // Bandbreite bevorzugt (z. B. Sync ↓/↑), sonst die erste Einheit
        const bw = nums.find(st => /bit\/s/.test(st.attributes.unit_of_measurement || ""));
        const u = (bw || nums[0] || { attributes: {} }).attributes.unit_of_measurement || "";
        const pair = nums.filter(st => (st.attributes.unit_of_measurement || "") === u).slice(0, 2);
        if (pair.length) info = pair.map(st => Math.round(parseFloat(st.state)).toLocaleString("de-DE")).join(" · ") + (u ? " " + u : "");
      }
      if (!info && w.backup && ph0.configured) info = ph0.reporting ? `${tr.phoneReady}${ph0.battery != null ? " · " + Math.round(ph0.battery) + " %" : ""}` : tr.phoneSilent;
      const nav = cfg.tap || cfg.navigation_path;
      return `<div class="line ${cls}"${nav ? ` data-nav="${esc(nav)}"` : ` data-a="detail" data-k="line" data-id="${esc(w.id)}"`} style="cursor:pointer">${isAct ? `<span class="tag">${tr.active}</span>` : ""}
        <span class="id">${esc(w.id)}</span><b>${esc(cfg.name || w.name)}</b><span class="st">${esc(label)}</span>${info ? `<div class="inf">${esc(info)}</div>` : ""}</div>`;
    }).join("");

    let status = "";
    if (s.planned && mode !== "normal") status = `<div class="box mut">${tr.plannedHint}</div>`;
    else if (s.assistant && s.assistant.kind === "start") status = this._assist(s, tr.assistTitle, "");
    else if (mode === "emergency") status = `<div class="box warn">${tr.hintEmergency}</div>`;
    if (mode === "dayflat" && s.assistant && s.assistant.steps.some(x => x.done === false)) status += this._assist(s, tr.assistTitle, "");
    if (mode === "normal" && s.assistant && s.assistant.kind === "return") status = this._assist(s, tr.returnTitle, tr.returnHint, true);
    if (mode === "normal" && s.pending_since && s.detect_delay > 0) {
      const left = Math.max(0, Math.round(s.detect_delay - (Date.now() - new Date(s.pending_since)) / 1000));
      status = `<div class="box warn">${tr.pending} <span id="pend" data-until="${new Date(new Date(s.pending_since).getTime() + s.detect_delay * 1000).toISOString()}">${left}</span> ${tr.seconds}</div>` + status;
    }
    else if (mode === "dayflat") status = `<div class="box ok timer"><div class="row1"><span>${tr.back}</span><span class="cd" id="cd">--:--:--</span></div>
      <div class="bar"><div id="bar" style="width:100%"></div></div>
      <div style="font-size:12px;margin-top:6px">${tr.flatUntil} ${when(s.flat_end)} · ${tr.restoreAt} ${when(s.restore_at)} · ${tr.orMain}</div></div>`;
    if (s.router_error) status += `<div class="box err">${tr.routerError}: ${esc(s.router_error)}${s.wan_missing ? ` <a href="/config/integrations/integration/homelines">${tr.openOptions}</a>` : ""}</div>`;
    if (this._feed && this._feed.state !== "ok" && this._feed.at) status = `<div class="box mut">${tr.reconnecting} ${hm(new Date(this._feed.at))}</div>` + status;

    const btns = [];
    if (mode === "emergency") btns.push(`<button class="b bp" data-a="ask-flat"><ha-icon icon="mdi:lock-open-variant"></ha-icon>${tr.unlock}</button>`);
    if (mode === "dayflat") btns.push(`<button class="b" data-a="ask-restrict"><ha-icon icon="mdi:lock"></ha-icon>${tr.restrict}</button>`);
    if (mode !== "normal" && s.tariff.booking_url) btns.push(`<a class="b" href="${esc(s.tariff.booking_url)}" target="_blank" rel="noreferrer"><ha-icon icon="mdi:cellphone"></ha-icon>${tr.book}</a>`);
    if (s.router_type !== "none") btns.push(`<button class="b" data-a="devices"><ha-icon icon="mdi:devices"></ha-icon>${tr.devices}</button>`);

    const c = s.counts || {};
    const u = s.usage || {};
    const be = u.breakeven_mb && mode === "emergency" && u.mb > u.breakeven_mb * 0.6
      ? `<div class="box warn">${tr.worthIt}: ${mb(u.breakeven_mb)} (${eur(s.tariff.dayflat_price)})</div>` : "";
    const metrics = `<div class="grid">
      <div class="m"><p class="ml">${tr.online}</p><p class="mv">${c.online_now ?? 0} / ${c.total ?? 0}</p></div>
      <div class="m"><p class="ml">${tr.since_reset} (${new Date(u.reset_at).toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit" })})</p><p class="mv">${mb(u.mb)}</p></div>
      <div class="m"><p class="ml">${tr.cost}</p><p class="mv">${eur(u.cost)}</p></div>
      <div class="m"><p class="ml">${tr.balance}</p><p class="mv">${eur(u.balance)}</p></div></div>`;

    const ic = (ok, warn) => ok === true ? `<ha-icon class="i-ok" icon="mdi:check-circle-outline"></ha-icon>` : ok === false ? `<ha-icon class="${warn ? "i-warn" : "i-err"}" icon="mdi:close-circle-outline"></ha-icon>` : `<ha-icon class="i-mut" icon="mdi:help-circle-outline"></ha-icon>`;
    const ph = s.phone || {};
    const backup = (s.wans || []).find(w => w.backup);
    let chain = "";
    if (ph.configured || backup) {
      const rows = [];
      if (ph.configured) {
        const a = agoMin(ph.last_seen);
        rows.push(`<div class="row"><span>${ic(ph.reporting)}${ph.reporting ? tr.phoneReports : tr.phoneSilent}${a !== null ? ` (${tr.ago} ${a} ${tr.min})` : ""}</span><span class="r">${ph.battery != null ? Math.round(ph.battery) + " %" : ""}${ph.charging ? " · lädt" : ""}</span></div>`);
        if (ph.mobile_data !== null) rows.push(`<div class="row"><span>${ic(ph.mobile_data)}${ph.mobile_data ? `${tr.mobile} ${esc(ph.operator || "")} ${esc(ph.network || "")}` : tr.dataOff}</span><span class="r">${ph.signal != null ? ph.signal + " dBm" : ""}</span></div>`);
        if (ph.charger !== null) rows.push(`<div class="row"><span>${ic(ph.usb, true)}${ph.usb ? tr.usb : tr.noUsb}</span><span class="r">${esc(ph.charger || "")}</span></div>`);
      }
      if (backup && s.standby === "cold" && mode === "normal" && backup.state !== "online") rows.push(`<div class="row"><span>${ic(null)}${tr.coldStandby}</span><span class="r">${esc(backup.name)}</span></div>`);
      else if (backup) rows.push(`<div class="row"><span>${ic(backup.state === "online", mode === "normal")}${backup.state === "online" ? tr.backupOnline : tr.backupOffline}</span><span class="r">${esc(backup.name)}</span></div>`);
      if (mode !== "normal") rows.push(`<div class="row"><span>${ic(mode === "dayflat")}${mode === "dayflat" ? tr.flatOn : tr.flatOff}</span><span class="r" id="tft">${mode === "dayflat" ? "" : `${String(s.tariff.price_per_mb).replace(".", ",")} ${tr.perMb}`}</span></div>`);
      chain = `<p class="sec">${tr.checklist}</p>${rows.join("")}`;
    }

    const mo = s.monitor || {};
    const lo = mo.last_outage;
    const rc = s.reconnect || {};
    const sp = (s.details || {}).speed || {};
    const spv = e => { const st = e && this._hass.states[e]; return st && !isNaN(parseFloat(st.state)) ? Math.round(parseFloat(st.state)).toLocaleString("de-DE") : null; };
    const spd = spv(sp.download), spu = spv(sp.upload);
    const mon = `<p class="sec" style="margin-top:12px">${tr.monitor} <span class="link" data-a="detail" data-k="outages">${tr.details}</span></p>
      ${spd != null ? `<div class="row" data-a="detail" data-k="speed" style="cursor:pointer"><span>${tr.speed}</span><span class="r">↓ ${spd}${spu != null ? ` · ↑ ${spu}` : ""} Mbit/s</span></div>` : ""}
      <div class="row"><span>${ic(mo.internet)}Internet</span><span class="r">${tr.latency} ${mo.latency != null ? mo.latency + " ms" : "–"}</span></div>
      <div class="row"><span>${tr.avail}</span><span class="r">${mo.availability_7d != null ? mo.availability_7d.toLocaleString("de-DE", { maximumFractionDigits: 2 }) + " %" : "–"}</span></div>
      <div class="row"><span>${tr.outages}</span><span class="r">${mo.outages_24h ?? 0} / ${mo.outages_7d ?? 0}</span></div>
      <div class="row"><span>${tr.lastOutage}</span><span class="r">${lo ? `${when(lo.start)} · ${dur(lo.duration)}` : tr.none}</span></div>
      ${rc.configured ? `<div class="row"><span>${ic(rc.result ? rc.result.startsWith("ok") : null)}${tr.reconnect} ${rc.enabled ? `${tr.next} ${rc.time}` : "aus"}</span>
        <span class="r">${rc.last ? `${tr.last} ${when(rc.last)}, ${tr.results[rc.result] || rc.result || ""}` : ""} ${mode === "normal" ? `<span class="link" data-a="reconnect">${tr.reconnectNow}</span>` : ""}</span></div>
        ${rc.error && rc.result !== "ok_new_ip" && rc.result !== "ok_same_ip" ? `<div class="e" style="margin:0 0 6px">${esc(rc.error)}</div>` : ""}` : ""}`;

    const compact = this._config.compact === true;
    const speedChip = spd != null ? `<span class="chip" data-a="detail" data-k="speed" style="cursor:pointer">↓ ${spd}${spu != null ? ` · ↑ ${spu}` : ""} Mbit/s</span>` : "";
    const chips = `<div class="chips">${speedChip}
      <span class="chip" data-a="detail" data-k="outages" style="cursor:pointer">${tr.latency} ${mo.latency != null ? String(mo.latency).replace(".", ",") + " ms" : "–"}</span>
      <span class="chip" data-a="detail" data-k="outages" style="cursor:pointer">${tr.avail} ${mo.availability_7d != null ? mo.availability_7d.toLocaleString("de-DE", { maximumFractionDigits: 2 }) + " %" : "–"}</span>
      <span class="chip" data-a="detail" data-k="outages" style="cursor:pointer">${tr.outages} ${mo.outages_24h ?? 0} / ${mo.outages_7d ?? 0}</span>
      <span class="chip" data-a="ask-reset" style="cursor:pointer">${u.cost ? `${tr.cost} ${eur(u.cost)} · ` : ""}${tr.balance} ${eur(u.balance)}</span></div>`;
    if (compact && mode === "normal" && !(s.assistant && s.assistant.kind === "return")) {
      this._main.innerHTML = `
      <div class="hd"><div class="t">${hlHead(title, sub)}</div>
      <span class="badge ${badgeCls}">${tr[mode]}</span></div>
      ${wans ? `<div class="lines">${wans}</div>` : ""}${status}${chips}${this._ov(s)}
      ${s.router_type !== "none" && this._config.show_devices !== false ? `<div class="btns" style="margin:10px 0 0">${btns.join("")}</div>` : ""}`;
      this._updateTimer(); this._mountTiles();
      if (this._view.dialog === "devices") this._renderDeviceList();
      return;
    }
    this._main.innerHTML = `
      <div class="hd"><div class="t">${hlHead(title, sub)}</div>
      <span class="badge ${badgeCls}">${tr[mode]}</span></div>
      ${wans ? `<div class="lines">${wans}</div>` : `<div style="height:12px"></div>`}
      ${status}${btns.length ? `<div class="btns">${btns.join("")}</div>` : ""}
      ${be}${metrics}
      <div class="sec" style="margin:-6px 0 8px;justify-content:flex-end"><span class="link" data-a="ask-reset">${tr.reset}</span></div>
      ${chain}${compact ? chips : mon}${this._ov(s)}`;
    this._updateTimer(); this._mountTiles();
    if (this._view.dialog === "devices") this._renderDeviceList();
  }

  _ov(s) {
    const n = (this._config.tiles || []).length;
    if (this._config.overview === false) return n ? hlOverview(s, this._hass, n, null) : "";
    return hlOverview(s, this._hass, n, this._config.overview_hide || {});
  }

  /* Eigene Kacheln (ab 0.8.6): „tiles:“ – homelines-tile-Einträge im selben Raster wie die Übersicht */
  _mountTiles() {
    const list = this._config.tiles || [];
    if (!list.length || !this._root) return;
    this._tileEls = this._tileEls || [];
    this._root.querySelectorAll(".hlovx").forEach(ph => {
      const i = Number(ph.dataset.ti), cfg = list[i]; if (!cfg) return;
      let el = this._tileEls[i];
      if (!el) {
        el = document.createElement("homelines-tile"); el._embedded = true;
        try { el.setConfig(cfg); } catch (err) { ph.textContent = String(err.message || err); return; }
        this._tileEls[i] = el;
      }
      if (this._hass) el.hass = this._hass;
      ph.appendChild(el);
    });
  }

  _openDetail(kind, wid) {
    if (!this._s) return;
    const spec = hlDetail(this._s, kind, wid);
    const el = document.createElement("homelines-detail"); el.hass = this._hass; el.open(this._s, kind, wid); this._detailEl = el;
    this._detail = hlOpenPopup(this._hass, null, null, { showCard: false, content: el, title: spec.title });
  }

  _assist(s, title, hint, ret = false) {
    const steps = s.assistant.steps;
    const items = steps.map((st, i) => {
      const cls = st.done === true ? "d" : st.done === false ? "x" : "u";
      const mark = st.done === true ? "✓" : String(i + 1);
      const extra = st.key === "book" && st.done !== true && s.mode === "emergency" ? ` <span class="link" data-a="ask-flat">${tr.unlock}</span>` : "";
      return `<li><span class="n ${cls}">${mark}</span><span>${tr.steps[st.key] || st.key}${st.done === null || st.done === undefined ? ` <small>(${tr.unchecked})</small>` : ""}${extra}</span></li>`;
    }).join("");
    return `<div class="box ${ret ? "mut" : "warn"}"><b style="font-weight:500">${title}</b>${hint ? `<div>${hint}</div>` : ""}<ul class="steps">${items}</ul>
      ${ret ? `<div style="text-align:right"><span class="link" data-a="dismiss-return">${tr.doneLink}</span></div>` : ""}</div>`;
  }

  _updateTimer() {
    const pend = this._root && this._root.getElementById("pend");
    if (pend) pend.textContent = Math.max(0, Math.round((new Date(pend.dataset.until) - Date.now()) / 1000));
    const s = this._s; if (!s || s.mode !== "dayflat" || !s.restore_at) return;
    const end = new Date(s.restore_at).getTime(); const start = new Date(s.booked_at).getTime();
    const left = Math.max(0, Math.round((end - Date.now()) / 1000));
    const h = Math.floor(left / 3600), m = Math.floor(left % 3600 / 60), sec = left % 60;
    const cd = this._root.getElementById("cd"); if (cd) cd.textContent = `${p2(h)}:${p2(m)}:${p2(sec)}`;
    const bar = this._root.getElementById("bar"); if (bar) bar.style.width = `${Math.max(0, Math.min(100, (end - Date.now()) / (end - start) * 100))}%`;
    const tft = this._root.getElementById("tft"); if (tft) tft.textContent = `noch ${p2(h)}:${p2(m)} h`;
  }

  /* ----------------------------------------------------------- Dialoge */
  _closeDialog() { this._view.dialog = null; this._dlg.innerHTML = ""; this._root.querySelector("ha-card").style.minHeight = ""; }
  _openDialog(name, minH = 420) { this._view.dialog = name; this._root.querySelector("ha-card").style.minHeight = `${minH}px`; }

  _askFlat() {
    this._openDialog("flat", 380);
    const now = new Date();
    this._dlg.innerHTML = `<div class="ov"><div class="dlg">
      <h3>${tr.confirmTitle}</h3><p>${tr.confirmBody}</p>
      <div class="fld"><label for="bt">${tr.bookedAt}</label><input id="bt" type="time" value="${hm(now)}"></div>
      <div class="pv" id="pv"></div>
      <label class="chk"><input type="checkbox" id="cb"> ${tr.iBooked}</label>
      <div class="e" id="er" hidden></div>
      <div class="acts"><button class="b" data-a="close">${tr.cancel}</button><button class="b bp" data-a="do-flat">${tr.confirm}</button></div></div></div>`;
    this._preview();
  }

  _bookedDate() {
    const v = this._root.getElementById("bt")?.value; if (!v) return null;
    const [h, m] = v.split(":").map(Number); const d = new Date(); d.setHours(h, m, 0, 0);
    if (d.getTime() > Date.now() + 60000) d.setDate(d.getDate() - 1);
    return d;
  }

  async _preview() {
    const d = this._bookedDate(); const pv = this._root.getElementById("pv"); if (!pv) return;
    if (!d) { pv.textContent = ""; return; }
    try {
      const r = await this._ws("homelines/preview", { booked_at: d.toISOString() });
      pv.textContent = `${tr.flatEnds} ${when(r.flat_end)} · ${tr.restoreAt} ${when(r.restore_at)}`;
    } catch (e) { pv.textContent = ""; }
  }

  _showErr(text) { const er = this._root.getElementById("er"); if (er) { er.textContent = text; er.hidden = false; } }

  async _doFlat() {
    const d = this._bookedDate();
    if (!d) return this._showErr(tr.errTime);
    if (!this._root.getElementById("cb").checked) return this._showErr(tr.errConfirm);
    try { await this._ws("homelines/activate_dayflat", { booked_at: d.toISOString() }); this._closeDialog(); }
    catch (e) { this._showErr(tr.errors[e.code] || e.message || String(e)); }
  }

  _askRestrict() {
    this._openDialog("restrict", 260);
    this._dlg.innerHTML = `<div class="ov"><div class="dlg"><h3>${tr.restrictTitle}</h3><p>${tr.restrictBody}</p>
      <div class="acts"><button class="b" data-a="close">${tr.cancel}</button><button class="b bp" data-a="do-restrict">${tr.restrict}</button></div></div></div>`;
  }

  _askReset() {
    this._openDialog("reset", 300);
    this._dlg.innerHTML = `<div class="ov"><div class="dlg"><h3>${tr.resetTitle}</h3><p>${tr.resetBody}</p>
      <div class="fld"><label for="nb">${tr.newBalance}</label><input id="nb" type="number" step="0.01" min="0" value="${(this._s.usage.balance ?? 0).toFixed(2)}" style="width:120px"></div>
      <div class="e" id="er" hidden></div>
      <div class="acts"><button class="b" data-a="close">${tr.cancel}</button><button class="b bp" data-a="do-reset">${tr.reset}</button></div></div></div>`;
  }

  _openDevices() {
    this._openDialog("devices", 640);
    const s = this._s;
    this._dlg.innerHTML = `<div class="ov"><div class="dlg">
      <div style="display:flex;justify-content:space-between;align-items:center"><h3>${tr.devTitle}</h3>
      <span><span class="link" data-a="refresh">${tr.refresh}</span> &nbsp; <ha-icon icon="mdi:close" data-a="close" style="cursor:pointer"></ha-icon></span></div>
      <div class="tabs">${s.supports_networks ? `<span class="tab" data-a="tab" data-v="networks">${tr.networks}</span>` : ""}<span class="tab" data-a="tab" data-v="devices">${tr.deviceList}</span>
        <span style="flex:1"></span>${["all", ...GROUPS].map(g => `<span class="tab" data-a="filter" data-v="${g}">${g === "all" ? tr.allGroups : gname(g)}</span>`).join("")}</div>
      <input type="search" id="q" placeholder="${tr.search}" value="${esc(this._view.q)}">
      <p class="pv" style="margin-top:6px">${tr.newDevices}: ${gname(s.default_group)}</p>
      <div class="list" id="dl"></div>
      <div class="acts"><button class="b bp" data-a="close">${tr.done}</button></div></div></div>`;
    this._renderDeviceList();
  }

  _renderDeviceList() {
    const box = this._root.getElementById("dl"); if (!box) return;
    const s = this._s; const v = this._view;
    this._root.querySelectorAll(".tab[data-a=tab]").forEach(t => t.classList.toggle("on", t.dataset.v === v.tab));
    this._root.querySelectorAll(".tab[data-a=filter]").forEach(t => t.classList.toggle("on", t.dataset.v === v.filter));
    const q = v.q.toLowerCase();
    const nets = Object.fromEntries((s.networks || []).map(n => [n.id, n.name]));
    let rows = [];
    if (v.tab === "networks") {
      rows = (s.networks || []).filter(n => (!q || n.name.toLowerCase().includes(q)) && (v.filter === "all" || (n.group || s.default_group) === v.filter))
        .map(n => {
          if (n.missing) return `<div class="row"><span class="dn">${esc(n.name)}<small class="i-warn">${tr.netMissing}</small></span><span class="seg"><span class="chip" data-a="grp" data-k="network" data-id="${esc(n.id)}" data-g="inherit">${tr.remove}</span></span></div>`;
          const chips = GROUPS.map(g => `<span class="chip ${n.group === g ? "on" : (!n.group && s.default_group === g ? "inh" : "")}" data-a="grp" data-k="network" data-id="${esc(n.id)}" data-g="${n.group === g ? "inherit" : g}">${gname(g)}</span>`).join("");
          return `<div class="row"><span class="dn">${esc(n.name)}<small>${n.group ? "" : tr.fromDefault}</small></span><span class="seg">${chips}</span></div>`;
        });
    } else {
      rows = (s.devices || []).filter(d => (!q || d.name.toLowerCase().includes(q) || d.id.toLowerCase().includes(q)) && (v.filter === "all" || d.group === v.filter))
        .map(d => {
          const explicit = d.source === "device";
          const chips = GROUPS.map(g => `<span class="chip ${d.group === g ? (explicit ? "on" : "inh") : ""}" data-a="grp" data-k="device" data-id="${esc(d.id)}" data-g="${explicit && d.group === g ? "inherit" : g}">${gname(g)}</span>`).join("");
          const info = [d.online ? "online" : "offline", d.network_id && nets[d.network_id] ? nets[d.network_id] : null,
            d.source === "network" ? tr.fromNet : d.source === "default" ? tr.fromDefault : null].filter(Boolean).join(" · ");
          return `<div class="row"><span class="dn">${esc(d.name)}<small>${esc(info)}</small></span><span class="seg">${chips}</span></div>`;
        });
    }
    box.innerHTML = rows.join("") || `<p class="pv">${tr.noDevices}</p>`;
  }

  /* ----------------------------------------------------------- Ereignisse */
  _onInput(e) {
    if (e.target.id === "q") { this._view.q = e.target.value; this._renderDeviceList(); }
    if (e.target.id === "bt") { const er = this._root.getElementById("er"); if (er) er.hidden = true; this._preview(); }
    if (e.target.id === "cb") { const er = this._root.getElementById("er"); if (er) er.hidden = true; }
  }

  async _onClick(e) {
    const navEl = e.target.closest("[data-nav]");
    if (navEl && !e.target.closest("[data-a]")) { hlNavigate(navEl.dataset.nav); return; }
    const det = e.target.closest("[data-a=detail]");
    if (det) { this._openDetail(det.dataset.k, det.dataset.id); return; }
    const el = e.target.closest("[data-a]"); if (!el) {
      if (e.target.classList?.contains("ov")) this._closeDialog();
      return;
    }
    const a = el.dataset.a;
    try {
      if (a === "ask-flat") this._askFlat();
      else if (a === "ask-restrict") this._askRestrict();
      else if (a === "ask-reset") this._askReset();
      else if (a === "devices") this._openDevices();
      else if (a === "close") this._closeDialog();
      else if (a === "do-flat") await this._doFlat();
      else if (a === "do-restrict") { await this._ws("homelines/restrict"); this._closeDialog(); }
      else if (a === "do-reset") {
        const v = parseFloat(this._root.getElementById("nb").value);
        await this._ws("homelines/reset_usage", isNaN(v) ? {} : { start_balance: v }); this._closeDialog();
      }
      else if (a === "tab") { this._view.tab = el.dataset.v; this._renderDeviceList(); }
      else if (a === "filter") { this._view.filter = el.dataset.v; this._renderDeviceList(); }
      else if (a === "grp") await this._ws("homelines/set_group", { kind: el.dataset.k, target: el.dataset.id, group: el.dataset.g });
      else if (a === "refresh") await this._ws("homelines/refresh");
      else if (a === "dismiss-return") await this._ws("homelines/dismiss_return");
      else if (a === "reconnect") await this._hass.callService("homelines", "reconnect", { entry_id: this._s.entry_id });
    } catch (err) {
      if (this._view.dialog) this._showErr(err.message || String(err));
      else console.error("HomeLines", err);
    }
  }
}

function hlNavigate(path) {
  if (!path) return;
  const target = path.startsWith("#") ? location.pathname + location.search + path : path;
  history.pushState(null, "", target);
  window.dispatchEvent(new CustomEvent("location-changed", { detail: { replace: false } }));
  if (path.startsWith("#")) window.dispatchEvent(new HashChangeEvent("hashchange"));
}

/* Kleine Kachel mit Text aus einer Vorlage und Warnfarben, z. B. für Detailseiten oder Popups */
const tileCss = `
:host{display:block;min-width:0;--hl-ok:var(--success-color,#2e7d32);--hl-warn:var(--warning-color,#f29d0b);--hl-err:var(--error-color,#db4437)}
ha-card{padding:10px 12px;display:flex;align-items:center;gap:12px;cursor:pointer;height:100%;box-sizing:border-box;border-width:1px}
ha-card.warn{border-color:var(--hl-warn);background:color-mix(in srgb,var(--hl-warn) 10%,var(--card-background-color,#fff))}
ha-card.err{border-color:var(--hl-err);background:color-mix(in srgb,var(--hl-err) 8%,var(--card-background-color,#fff))}
.ic{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:color-mix(in srgb,var(--secondary-text-color) 12%,transparent);color:var(--secondary-text-color)}
.warn .ic{background:color-mix(in srgb,var(--hl-warn) 22%,transparent);color:color-mix(in srgb,var(--hl-warn) 75%,var(--primary-text-color))}
.err .ic{background:color-mix(in srgb,var(--hl-err) 18%,transparent);color:var(--hl-err)}
.tx{min-width:0;flex:1}
.n{font-size:14px;font-weight:500;color:var(--primary-text-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.s{font-size:12px;color:var(--secondary-text-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.warn .s{color:color-mix(in srgb,var(--hl-warn) 75%,var(--primary-text-color))}.err .s{color:var(--hl-err)}
.ch{color:var(--secondary-text-color);--mdc-icon-size:20px}
ha-card.emb{box-shadow:none;border:1px solid var(--divider-color);border-radius:12px;background:none}
ha-card.emb.warn{border-color:var(--hl-warn);background:color-mix(in srgb,var(--hl-warn) 10%,transparent)}
ha-card.emb.err{border-color:var(--hl-err);background:color-mix(in srgb,var(--hl-err) 8%,transparent)}
.emb .s{font-size:13px}`;

class HomeLinesTile extends HTMLElement {
  setConfig(c) {
    if (!c || !c.name) throw new Error("name fehlt");
    this._c = c; this._v = {}; this._unsub();
    if (this._hass) this._sub();
  }
  static getStubConfig() { return { name: "Bereich", icon: "mdi:information-outline" }; }
  getCardSize() { return 1; }
  getGridOptions() { return { columns: 6, rows: 1, min_columns: 4 }; }
  set hass(h) {
    const first = !this._hass; this._hass = h; if (!this.shadowRoot) this._build(); if (first) this._sub();
    if (this._pop && this._pop.open) this._pop.setHass(h);
    const key = (this._c.entities || []).map(e => h.states[e] && h.states[e].state).join("|");
    if (key !== this._key && !this._edit) { this._key = key; this._paint(); }
  }
  connectedCallback() { if (this._hass && !(this._subs || []).length) this._sub(); }
  /* Ohne Vorlagen (ab 0.8.4): Text und Farbe aus den gewählten Entitäten */
  _calc() {
    const c = this._c, h = this._hass, ents = c.entities || [];
    if (!ents.length || !h) return null;
    const sts = ents.map(e => h.states[e]);
    const bad = sts.filter(st => !st || ["unavailable", "unknown"].includes(st.state)).length;
    const nums = sts.map(st => st ? parseFloat(st.state) : NaN).filter(v => !isNaN(v));
    const unit = c.unit ?? ((sts.find(st => st && st.attributes.unit_of_measurement) || { attributes: {} }).attributes.unit_of_measurement || "");
    const f = v => hlNum(v, unit, c.decimals).replace(unit ? " " + unit : /$^/, "");
    const mode = c.combine || (ents.length > 1 ? "sum" : "single");
    let val = null, text;
    if (mode === "list") text = ents.map(e => hlFmt(h, e) ?? "–").join(" · ");
    else if (mode === "single") { const st = sts[0]; const v = st ? parseFloat(st.state) : NaN; val = isNaN(v) ? null : v; text = !isNaN(v) ? `${f(v)}${unit ? " " + unit : ""}` : (st ? st.state : "–"); }
    else if (nums.length) {
      val = mode === "min" ? Math.min(...nums) : mode === "max" ? Math.max(...nums) : mode === "avg" ? nums.reduce((a, b) => a + b, 0) / nums.length : nums.reduce((a, b) => a + b, 0);
      text = `${f(val)}${unit ? " " + unit : ""}${mode === "sum" && ents.length > 1 ? " gesamt" : ""}`;
    } else text = "–";
    if (bad && c.warn_unavailable) text += ` · ${bad} nicht erreichbar`;
    const num = x => (x === undefined || x === null || x === "" ? null : Number(x));
    const out = (lo, hi) => val != null && ((num(lo) != null && val < num(lo)) || (num(hi) != null && val > num(hi)));
    const err = out(c.error_below, c.error_above), warn = !err && ((bad > 0 && c.warn_unavailable) || out(c.warn_below, c.warn_above));
    return { text, err, warn };
  }
  disconnectedCallback() { this._unsub(); }
  _build() {
    this.attachShadow({ mode: "open" }).innerHTML = `<style>${tileCss}</style><ha-card><div class="ic"><ha-icon></ha-icon></div><div class="tx"><div class="n"></div><div class="s"></div></div><ha-icon class="ch" icon="mdi:chevron-right"></ha-icon></ha-card>`;
    this.shadowRoot.querySelector("ha-card").addEventListener("click", () => {
      const c = this._c, ta = c.tap_action || {};
      if (c.navigation_path || ta.navigation_path) hlNavigate(c.navigation_path || ta.navigation_path);
      else if ((c.entities || []).length) {
        const el = document.createElement("homelines-detail");
        el.hass = this._hass; el.open(null, "entities", { title: c.name, key: c.window, entities: c.entities, hours: Number(c.hours) || 24 });
        this._pop = hlOpenPopup(this._hass, null, null, { showCard: false, content: el, title: c.name });
      }
      else if (c.entity) this.dispatchEvent(new CustomEvent("hass-more-info", { bubbles: true, composed: true, detail: { entityId: c.entity } }));
    });
    this._paint();
  }
  _unsub() { (this._subs || []).forEach(p => p.then(u => u && u()).catch(() => {})); this._subs = []; }
  _sub() {
    this._unsub();
    ["text", "warning", "error"].forEach(k => {
      if (!this._c || this._c[k] == null) return;
      this._subs.push(this._hass.connection.subscribeMessage(r => {
        if (r && "result" in r) { this._v[k] = r.result; this._paint(); }
      }, { type: "render_template", template: String(this._c[k]) }));
    });
  }
  _paint() {
    if (!this.shadowRoot || !this._c) return;
    const truthy = v => v === true || ["true", "on", "1", "yes", "ja"].includes(String(v ?? "").trim().toLowerCase());
    const calc = this._calc();
    let err = truthy(this._v.error), warn = !err && truthy(this._v.warning);
    if (calc && this._c.error == null && calc.err) err = true;
    if (calc && !err && this._c.warning == null && calc.warn) warn = true;
    const card = this.shadowRoot.querySelector("ha-card");
    card.className = [this._embedded ? "emb" : "", err ? "err" : warn ? "warn" : ""].filter(Boolean).join(" ");
    this.shadowRoot.querySelector(".ic ha-icon").setAttribute("icon", err || warn ? (this._c.warning_icon || "mdi:alert-outline") : (this._c.icon || "mdi:information-outline"));
    this.shadowRoot.querySelector(".n").textContent = this._c.name;
    const txt = this._c.text != null ? this._v.text : (calc ? calc.text : null);
    this.shadowRoot.querySelector(".s").textContent = txt == null ? "" : String(txt);
    this.shadowRoot.querySelector(".ch").style.display = (this._c.navigation_path || (this._c.tap_action || {}).navigation_path || (this._c.entities || []).length) ? "" : "none";
  }
}

/* ------------------------------------------------------------------ Mini-Karte
   type: custom:homelines-mini
   layout: bar | tile            (Leiste über die ganze Breite oder kleine Kachel)
   name: Internet                (optional)
   throughput_entity: sensor.…   (optional, Verlauf als Sparkline, z. B. UniFi „WAN Download“)
   upload_entity: sensor.…       (optional, zweite Linie in Blau, z. B. „WAN Upload“)
   throughput_hours: 6           (optional)
   info: "{{ … }}"               (optional, ersetzt die zweite Zeile im Normalbetrieb)
   navigation_path: "#internet"  (optional, statt des eingebauten Popups)
   card: { lines: … }            (optional, Einstellungen für die große Karte im Popup)
   popup_view: /dashboard-x/internet (optional, vorhandene Dashboard-Seite als Modal)
   popup_cards: [ … ]            (optional, weitere Karten im Popup, z. B. Detail-Kacheln)
   popup_columns: 2              (optional)
   popup_show_card: false        (optional, HomeLines-Karte im Popup weglassen)          */
const miniCss = `
:host{display:block;--hl-ok:var(--success-color,#2e7d32);--hl-warn:var(--warning-color,#f29d0b);--hl-err:var(--error-color,#db4437);--hl-acc:var(--primary-color,#03a9f4)}
ha-card{cursor:pointer;height:100%;box-sizing:border-box;overflow:hidden;container-type:inline-size;-webkit-tap-highlight-color:transparent;position:relative}
ha-card.warn{border-color:var(--hl-warn)}ha-card.err{border-color:var(--hl-err)}
.w{display:flex;align-items:center;gap:12px;padding:10px 12px;height:100%;box-sizing:border-box;position:relative;z-index:1}
.ic{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:color-mix(in srgb,var(--c) 18%,transparent);color:var(--c);--mdc-icon-size:22px}
.tx{min-width:0;flex:1}
.n{font-size:14px;font-weight:500;color:var(--primary-text-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;align-items:center;gap:6px}
.s{font-size:12.5px;color:var(--secondary-text-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-variant-numeric:tabular-nums;margin-top:1px}
.pill{font-size:11px;font-weight:500;padding:1px 8px;border-radius:9px;background:var(--hl-acc);color:var(--text-primary-color,#fff);flex-shrink:0}
.dots{display:flex;gap:5px;flex-shrink:0}
.d{width:9px;height:9px;border-radius:50%;background:color-mix(in srgb,var(--secondary-text-color) 35%,transparent);box-sizing:border-box}
.d.a{background:var(--hl-ok);box-shadow:0 0 0 2px color-mix(in srgb,var(--hl-ok) 30%,transparent)}
.d.o{background:color-mix(in srgb,var(--hl-ok) 55%,transparent)}.d.x{background:var(--hl-err)}
.d.na{background:none;border:1.5px dashed color-mix(in srgb,var(--secondary-text-color) 60%,transparent)}
.w .tx{flex:0 1 auto}
.w svg.sp{flex:1 1 0;min-width:0;max-width:220px;height:30px;overflow:visible}
@container (max-width:300px){.w svg.sp{display:none}}
.ch{color:var(--secondary-text-color);--mdc-icon-size:20px;flex-shrink:0;margin-left:-4px}
@container (max-width:240px){.w .dots{display:none}}
/* Kachel */
.t{display:flex;flex-direction:column;padding:12px;gap:6px;height:100%;box-sizing:border-box}
.t .top{display:flex;justify-content:space-between;align-items:flex-start}
.t .s{white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.t svg.sp{display:block;width:100%;height:28px;margin-top:auto}
`;
const popCss = `
.hl-pop{position:fixed;inset:0;z-index:1000;display:flex;align-items:flex-start;justify-content:center;background:rgba(0,0,0,.5);overflow:auto;padding:5vh 12px 24px;box-sizing:border-box;animation:lgf .15s ease-out}
.hl-pop .in{width:min(620px,100%);position:relative}
.hl-pop .in.wide{width:min(1000px,100%)}
.hl-pop .grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:8px;margin-top:8px}
.hl-pop .grid>:first-child{margin-top:0}
.hl-pop .err{background:var(--card-background-color,#fff);color:var(--error-color,#db4437);padding:10px;border-radius:12px;grid-column:1/-1}
.hl-pop .hl-x{position:absolute;right:6px;top:-44px;width:38px;height:38px;border-radius:50%;border:0;cursor:pointer;background:var(--card-background-color,#fff);color:var(--primary-text-color);font-size:20px;line-height:38px;box-shadow:0 2px 8px rgba(0,0,0,.3)}
@media (max-width:600px){.hl-pop{padding:56px 8px 16px;align-items:flex-start}.hl-pop .in{width:100%}}
@media (max-width:600px){.hl-pop .grid>*{grid-column:1 / -1 !important}}
@keyframes lgf{from{opacity:0}to{opacity:1}}
.hl-pop .pt{margin:4px 40px 10px 4px;font-size:18px;font-weight:500;color:var(--primary-text-color)}
.hl-pop .in.panel{background:var(--primary-background-color,#fafafa);border-radius:16px;padding:14px 14px 16px;box-sizing:border-box}
`;
/* Übersicht (ab 0.8.4): je eine Zeile für Notfall-Strecke, Leitungen mit Detailwerten, Geschwindigkeit
   und Ausfälle – Werte auf einen Blick, Tipp öffnet das passende Detailfenster */
function hlFmt(hass, e) {
  const st = e && hass.states[e]; if (!st || ["unavailable", "unknown"].includes(st.state)) return null;
  const v = parseFloat(st.state), u = st.attributes.unit_of_measurement || "";
  if (!isNaN(v) && /^-?[\d.]+$/.test(st.state)) return hlNum(v, u);
  if (e.startsWith("button.")) return null;
  return st.state;
}
function hlOverview(s, hass, extra = 0, hide = {}) {
  // hide === null: nur die eigenen Kacheln (Übersicht aus)
  if (hide === null) hide = new Proxy({}, { get: () => true });
  const d = s.details || {}, rows = [], mode = s.mode, ph = s.phone || {}, u = s.usage || {}, mo = s.monitor || {};
  const backup = (s.wans || []).find(w => w.backup);
  if (backup && !hide.backup) {
    let t, cls = "";
    if (mode !== "normal") { t = `Notbetrieb · ${mb(u.mb)} · ${eur(u.cost)}`; cls = "warn"; }
    else if (ph.configured) { t = ph.reporting ? `Handy bereit${ph.battery != null ? " · " + Math.round(ph.battery) + " %" : ""}` : "Handy meldet sich nicht"; if (!ph.reporting) cls = "err"; }
    else t = backup.state === "online" ? "Backup online" : "Backup in Bereitschaft";
    (d.backup || []).slice(0, 1).forEach(e => { const v = hlFmt(hass, e); if (v) t += ` · ${v}`; });
    rows.push({ k: "line", id: backup.id, icon: "mdi:cellphone-link", n: "Notfall-Strecke", t, cls });
  }
  (s.wans || []).filter(w => !w.backup && !hide[w.id] && ((d.lines || {})[w.id] || {}).entities && d.lines[w.id].entities.length).forEach(w => {
    const vals = d.lines[w.id].entities.map(e => hlFmt(hass, e)).filter(Boolean).slice(0, 2);
    rows.push({ k: "line", id: w.id, icon: "mdi:router-network", n: w.name || w.id, t: vals.join(" · ") || "–",
      cls: w.state === "offline" && w.primary ? "err" : "" });
  });
  const sp = d.speed || {};
  if (sp.download && !hide.speed) {
    const r0 = e => { const st = e && hass.states[e], v = st ? parseFloat(st.state) : NaN; return isNaN(v) ? null : `${Math.round(v).toLocaleString("de-DE")} ${st.attributes.unit_of_measurement || ""}`.trim(); };
    const dn = r0(sp.download), up = r0(sp.upload);
    rows.push({ k: "speed", icon: "mdi:speedometer", n: "Geschwindigkeit", t: [dn && "↓ " + dn, up && "↑ " + up].filter(Boolean).join(" · ") || "–" });
  }
  const av = mo.availability_7d != null ? mo.availability_7d.toLocaleString("de-DE", { maximumFractionDigits: 2 }) + " %" : "–";
  if (!hide.outages) rows.push({ k: "outages", icon: "mdi:lan-disconnect", n: "Ausfälle und Verlauf",
    t: `${mo.outages_24h ?? 0} / ${mo.outages_7d ?? 0} / ${mo.outages_30d ?? 0} · ${av}`,
    cls: mo.internet === false ? "err" : (mo.outages_24h || 0) > 0 ? "warn" : "" });
  return `<div class="hlovw">${rows.map(r => `<div class="hlov ${r.cls || ""}" data-a="detail" data-k="${r.k}"${r.id ? ` data-id="${esc(r.id)}"` : ""}>
    <div class="hlov-i"><ha-icon icon="${r.cls ? (r.cls === "err" ? "mdi:alert-circle-outline" : "mdi:alert-outline") : r.icon}"></ha-icon></div>
    <div class="hlov-t"><div class="hlov-n">${esc(r.n)}</div><div class="hlov-s">${esc(r.t)}</div></div><ha-icon class="hlov-c" icon="mdi:chevron-right"></ha-icon></div>`).join("")}${Array.from({ length: extra }, (_, i) => `<div class="hlovx" data-ti="${i}"></div>`).join("")}</div>`;
}
function hlOverviewEntities(s) {
  const d = (s && s.details) || {};
  return [...Object.values(d.lines || {}).flatMap(l => l.entities || []), (d.speed || {}).download, (d.speed || {}).upload, ...(d.backup || [])].filter(Boolean);
}

/* Eingebaute Detailfenster (ab 0.8.0): aus den HomeLines-Optionen, ohne eigene Dashboard-Seite */
/* Detailfenster (ab 0.8.5): Bausteine statt fertiger HA-Karten.
   values    – Felder mit Name und Wert (Tipp: HA-Detailfenster)
   chart     – Verlauf; Werte mit gleicher Einheit in einem Diagramm mit Legende
   timeline  – Zustände als Streifen (z. B. Internet an/aus, Betriebsart)
   controls  – Schalter und Knöpfe (HA-Liste)
   phone     – Prüfliste Notfall-Handy, log – Ausfall-Protokoll, hint – Hinweis */
const HL_CTL = /^(button|switch|input_[a-z]+|time|select|number|script|automation)\./;
function hlDetailDefault(s, kind, wid) {
  const d = s.details || {}, own = d.own || {}, blocks = [];
  const uniq = arr => [...new Set((arr || []).filter(Boolean))];
  const vals = arr => uniq(arr).filter(e => !HL_CTL.test(e));
  const ctls = arr => uniq(arr).filter(e => HL_CTL.test(e));
  const push = (type, o) => { if (o.entities && !o.entities.length) return; blocks.push({ type, ...o }); };
  if (kind === "line") {
    const w = (s.wans || []).find(x => x.id === wid) || { id: wid, name: wid };
    const ld = (d.lines || {})[wid] || {};
    if (w.backup) {
      push("phone", {});
      push("values", { entities: vals([own.status, ...(ld.entities || []), ...(d.backup || []), own.usage, own.cost, own.balance, own.devices_online]) });
      push("controls", { title: "Aktionen", entities: ctls([own.test_notify, own.reset_usage, ...(ld.entities || []), ...(d.backup || [])]) });
      push("chart", { entities: uniq(ld.history), hours: 720 });
      push("timeline", { title: "Notbetrieb – 30 Tage", entities: uniq([own.status]), hours: 720 });
    } else {
      if (!(ld.entities || []).length && !(ld.history || []).length)
        push("hint", { text: w.entity_id ? "Für diese Leitung sind keine Detailwerte eingestellt (HomeLines → Konfigurieren → Detailansichten der Karte)."
          : "Noch nicht angeschlossen. Sobald die Leitung im Router läuft, erscheinen hier Status und Werte – Sensoren dafür unter HomeLines → Konfigurieren → Detailansichten der Karte." });
      push("values", { entities: vals([w.entity_id, ...(ld.entities || [])]) });
      push("chart", { entities: uniq(ld.history), hours: 720 });
      const rc = w.primary && s.reconnect && s.reconnect.configured
        ? ["daily_reconnect", "reconnect_time", "last_reconnect", "reconnect_result", "wan_ip", "reconnect_now"].map(k => own[k]) : [];
      push("controls", { title: rc.length ? "Neueinwahl" : "Bedienung", entities: ctls([...rc.filter(e => HL_CTL.test(e)), ...(ld.entities || [])])
        .concat(rc.filter(e => e && !HL_CTL.test(e))) });
    }
    return { title: w.name && w.name !== w.id ? `${w.name} (${w.id})` : w.id, blocks };
  }
  if (kind === "speed") {
    const sp = d.speed || {};
    push("values", { entities: vals([sp.download, sp.upload, ...(sp.extra || [])]) });
    push("controls", { title: "Bedienung", entities: ctls(sp.extra) });
    push("chart", { title: "Speedtest – 30 Tage", entities: uniq([sp.download, sp.upload]), hours: 720 });
    return { title: "Geschwindigkeit", blocks };
  }
  if (kind === "entities") {
    push("values", { entities: vals(wid.entities) });
    push("controls", { title: "Bedienung", entities: ctls(wid.entities) });
    push("chart", { entities: vals(wid.entities), hours: wid.hours || 24 });
    return { title: wid.title, blocks };
  }
  const prim = (s.wans || []).find(w => w.primary);
  push("values", { entities: vals([own.internet, own.router, own.outages_24h, own.outages_7d, own.outages_30d, own.availability_7d, own.downtime_7d, own.last_check, ...(d.monitor || [])]) });
  push("log", {});
  push("timeline", { title: "Verbindung – 24 Stunden", entities: uniq([own.internet, own.router, prim && prim.entity_id, d.active_wan_entity, own.status]), hours: 24 });
  push("chart", { title: "Latenz – 24 Stunden", entities: uniq([own.latency, ...(d.monitor || [])]), hours: 24 });
  push("chart", { title: "Paketverlust – 30 Tage", entities: uniq([own.packet_loss]), hours: 720 });
  push("controls", { title: "Bedienung", entities: ctls(d.monitor) });
  return { title: "Ausfälle und Verlauf", blocks };
}

/* ================================================================ Fenster-Baukasten (ab 0.9.0)
   Jedes Fenster ist eine Liste von Bausteinen. Hat der Nutzer ein Fenster angepasst, speichert die
   Integration es unter einem Schlüssel (Leitung: WAN2, „speed“, „outages“, eigene Kachel: „t-strom“).
   Sonst zeigt HomeLines das eingebaute Fenster wie bisher. */
const HL_NAMED = { blue: "#4469d0", orange: "#e8b33f", red: "#e9735a", green: "#5fb7a0", purple: "#9b6ad6", teal: "#4fa7d8", pink: "#c75c8a", gray: "#8a9099" };
const HL_COLOR_N = { blue: "Blau", orange: "Gelb", red: "Rot", green: "Grün", purple: "Lila", teal: "Türkis", pink: "Rosa", gray: "Grau" };
const HL_BLK = { values: ["mdi:view-grid-outline", "Werte"], chart: ["mdi:chart-line", "Grafik"], actions: ["mdi:gesture-tap-button", "Schalter und Aktionen"],
  log: ["mdi:format-list-bulleted", "Protokoll"], text: ["mdi:information-outline", "Hinweistext"], phone: ["mdi:cellphone-check", "Prüfliste Notfall-Handy"] };
const HL_BLK_D = { values: "aktuelle Werte, mit Warnfarben", chart: "Linie, Fläche, Balken oder An/Aus-Streifen", actions: "Schalter, Uhrzeit, Knöpfe",
  log: "Ausfälle, Notbetrieb, Neueinwahl", text: "kurzer Hinweis, neutral, gelb oder rot", phone: "Kabel, Mobilfunk, mobile Daten" };
const HL_HOURS = { "24h": 24, "7d": 168, "30d": 720 };
const HL_RANGE_N = [["24h", "24 h"], ["7d", "7 Tage"], ["30d", "30 Tage"]];
const HL_KIND_N = [["line", "Linie"], ["area", "Fläche"], ["bar", "Balken"], ["strip", "An/Aus-Streifen"]];
const HL_WHEN_N = [["unavail", "nicht erreichbar ist"], ["below", "unter"], ["above", "über"], ["is", "gleich"], ["isnot", "nicht gleich"]];
const HL_LOG_N = [["outages", "Ausfälle"], ["switch", "Notbetrieb (Umschaltungen)"], ["reconnect", "Letzte Neueinwahl"]];
const HL_GRP_N = { all: "Wert", phone: "Rufnummer", battery: "Batterie", power: "Steckdose", connectivity: "Gerät", temperature: "Fühler" };
const hlRangeOf = h => (h >= 720 ? "30d" : h >= 168 ? "7d" : "24h");
function hlSlug(n) {
  return String(n || "").toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 36) || "kachel";
}
function hlWinKey(kind, wid) {
  if (kind === "line") return String(wid);
  if (kind === "entities") return (wid && wid.key) || `t-${hlSlug(wid && wid.title)}`;
  return kind;   // speed, outages
}
function hlFromStored(list) {
  return (list || []).map(b => {
    const ents = b.ents || [];
    if (b.t === "values") return { type: "values", title: b.title, entities: ents, rules: b.rules || [], style: b.style };
    if (b.t === "chart") return b.kind === "strip" ? { type: "timeline", title: b.title, entities: ents, hours: HL_HOURS[b.range] || 24 }
      : { type: "chart", title: b.title, entities: ents, hours: HL_HOURS[b.range] || 24, kind: b.kind, mode: b.mode, colors: b.colors || {}, limit: b.limit, stats: b.stats };
    if (b.t === "actions") return { type: "controls", title: b.title, entities: ents };
    if (b.t === "log") return { type: "log", title: b.title, src: b.src, n: b.n, style: b.style };
    if (b.t === "text") return { type: "hint", text: b.text, tone: b.tone };
    if (b.t === "phone") return { type: "phone" };
    return null;
  }).filter(Boolean);
}
const HL_NOLIMIT = () => ({ on: false, v: "", dir: "below", c: "warn" });
function hlToStored(blocks) {
  return (blocks || []).map(b => {
    const ents = [...(b.entities || [])];
    if (b.type === "values") return { t: "values", title: b.title || "", ents, rules: b.rules || [], style: b.style || "tiles" };
    if (b.type === "chart") return { t: "chart", title: b.title || "", ents, kind: b.kind || "line", range: hlRangeOf(b.hours || 24), mode: b.mode || "together",
      colors: { ...(b.colors || {}) }, limit: { ...HL_NOLIMIT(), ...(b.limit || {}) }, stats: !!b.stats };
    if (b.type === "timeline") return { t: "chart", title: b.title || "", ents, kind: "strip", range: hlRangeOf(b.hours || 24), mode: "together", colors: {}, limit: HL_NOLIMIT(), stats: false };
    if (b.type === "controls") return { t: "actions", title: b.title || "", ents };
    if (b.type === "log") return { t: "log", title: b.title || "Ausfälle", src: b.src || "outages", n: b.n || 20, style: b.style || "list" };
    if (b.type === "hint") return { t: "text", text: b.text || "", tone: b.tone || "info" };
    if (b.type === "phone") return { t: "phone", title: "" };
    return null;
  }).filter(Boolean);
}
function hlDetail(s, kind, wid) {
  const st = s || {}, def = hlDetailDefault(st, kind, wid), key = hlWinKey(kind, wid);
  const own = (st.windows || {})[key];
  return { ...def, key, kind, wid, custom: !!own, blocks: own ? hlFromStored(own) : def.blocks, defaults: def.blocks };
}
/* Warnfarben als Sätze: „Rot, wenn eine Rufnummer nicht gleich registered“ */
function hlGrp(h, e) {
  const st = h && h.states[e], dc = st && st.attributes.device_class;
  if (/rufnummer|phone_number|_number_\d+_status/.test(e)) return "phone";
  return dc || "other";
}
function hlRuleHit(h, r, e) {
  if (r.grp && r.grp !== "all" && hlGrp(h, e) !== r.grp) return null;
  const st = h && h.states[e]; if (!st) return null;
  const na = ["unavailable", "unknown"].includes(st.state);
  if (r.when === "unavail") return na;
  if (na) return false;
  const n = parseFloat(st.state), v = parseFloat(String(r.v).replace(",", "."));
  if (r.when === "below") return !isNaN(n) && n < v;
  if (r.when === "above") return !isNaN(n) && n > v;
  if (r.when === "is") return String(st.state) === String(r.v);
  if (r.when === "isnot") return String(st.state) !== String(r.v);
  return false;
}
function hlLevel(h, rules, ents) {
  let lvl = "";
  for (const r of rules || []) {
    const res = ents.map(e => hlRuleHit(h, r, e)).filter(x => x !== null);
    const hit = res.length && (r.any === "all" ? res.every(Boolean) : res.some(Boolean));
    if (hit) { if (r.c === "err") return "err"; lvl = "warn"; }
  }
  return lvl;
}
/* FRITZ!Box-Vorlage: sucht die Werte über die Integrationen, nicht über feste Namen */
function hlFritzTemplate(h) {
  const reg = (h && h.entities) || {}, all = Object.keys((h && h.states) || {});
  const plat = e => (reg[e] && reg[e].platform) || "";
  const sorted = a => a.sort((x, y) => x.localeCompare(y, "de", { numeric: true }));
  const phones = sorted(all.filter(e => e.startsWith("sensor.") && /rufnummer_?\d*_status$|phone_number_?\d*_status$/.test(e)));
  const dect = sorted(all.filter(e => plat(e) === "fritzbox" && e.startsWith("sensor.") && (/_batterie$|_battery$/.test(e) || (h.states[e].attributes.device_class === "battery"))));
  const ping = sorted(all.filter(e => plat(e) === "ping" && e.startsWith("binary_sensor.")));
  const fritz = all.filter(e => plat(e) === "fritz");
  const router = [
    ...fritz.filter(e => e.startsWith("sensor.") && h.states[e].attributes.device_class === "temperature"),
    ...fritz.filter(e => /letzter_neustart|last_restart|uptime/.test(e)),
    ...fritz.filter(e => e.startsWith("update.")),
  ];
  const blocks = [];
  if (phones.length) blocks.push({ t: "values", title: "Telefonie", ents: phones, rules: [{ c: "err", any: "any", grp: "all", when: "isnot", v: "registered" }], style: "list" });
  if (dect.length) blocks.push({ t: "values", title: "Heizung (DECT)", ents: dect, rules: [{ c: "err", any: "any", grp: "all", when: "unavail", v: "" }, { c: "warn", any: "any", grp: "all", when: "below", v: "20" }], style: "list" });
  if (ping.length) blocks.push({ t: "values", title: "WLAN-Geräte", ents: ping, rules: [{ c: "err", any: "any", grp: "all", when: "is", v: "off" }], style: "list" });
  if (router.length) blocks.push({ t: "values", title: "Router", ents: [...new Set(router)].slice(0, 6), rules: [], style: "tiles" });
  const temp = router.find(e => h.states[e].attributes.device_class === "temperature");
  if (temp) blocks.push({ t: "chart", title: "CPU-Temperatur", ents: [temp], kind: "line", range: "7d", mode: "together", colors: {}, limit: { on: true, v: "80", dir: "above", c: "warn" }, stats: true });
  return blocks;
}

function hlMoreInfo(entityId) {
  // Das HA-Detailfenster hört auf <home-assistant>; unsere Fenster hängen direkt am <body> und lägen
  // darüber. Deshalb treten sie zur Seite, bis das HA-Fenster wieder zu ist.
  const ha = document.querySelector("home-assistant");
  if (!ha) return;
  const pops = [...document.querySelectorAll("body > .hl-pop")];
  pops.forEach(p => { p.style.visibility = "hidden"; });
  ha.dispatchEvent(new CustomEvent("hass-more-info", { bubbles: true, composed: true, detail: { entityId } }));
  const dlg = () => ha.shadowRoot && ha.shadowRoot.querySelector("ha-more-info-dialog");
  let seen = false;
  const t0 = Date.now();
  const t = setInterval(() => {
    const d = dlg(), open = !!(d && (d.open || d._open || (d.shadowRoot && d.shadowRoot.querySelector("[open]"))) && d.isConnected);
    if (open) seen = true;
    if ((seen && !open) || (!seen && Date.now() - t0 > 4000)) { clearInterval(t); pops.forEach(p => { p.style.visibility = ""; }); }
  }, 250);
}

/* Kurze Namen: was alle Namen eines Bausteins vorne oder hinten gemeinsam haben, fällt weg
   („Modem DSL Sync Download“, „Modem DSL Rauschabstand Download“ → „Sync Download“, „Rauschabstand Download“) */
/* Technische Zusätze aus Gerätenamen entfernen (ab 0.8.6):
   „Gerät (Adresse / Netz) Gerät Status“ → „Gerät Status“ */
function hlCleanName(n) {
  let x = String(n || "").replace(/\s*\((?=[^)]*(?:\s\/\s|\d+\.\d+\.\d+))[^)]*\)/g, "").replace(/\s+/g, " ").trim();
  const w = x.split(" ");
  for (let k = Math.floor(w.length / 2); k >= 1; k--) {
    if (w.slice(0, k).join(" ") === w.slice(k, 2 * k).join(" ")) { x = w.slice(k).join(" "); break; }
  }
  return x || String(n || "");
}
function hlShortNames(names) {
  if (names.length < 2) return names;
  const w = names.map(n => String(n).split(/\s+/));
  // Vorne: Namen mit gleichem Anfang (z. B. „HomeLines …“, „Modem DSL …“) gruppenweise kürzen
  const groups = {};
  w.forEach((x, i) => { (groups[x[0]] = groups[x[0]] || []).push(i); });
  const pre = w.map(() => 0);
  Object.values(groups).filter(g => g.length > 1).forEach(g => {
    const min = Math.min(...g.map(i => w[i].length));
    let p = 0;
    while (p < min - 1 && g.every(i => w[i][p] === w[g[0]][p])) p++;
    g.forEach(i => { pre[i] = p; });
  });
  // Hinten nur, was wirklich alle gemeinsam haben (z. B. „… Leistung“)
  let suf = 0;
  const min = Math.min(...w.map((x, i) => x.length - pre[i]));
  while (suf < min - 1 && w.every(x => x[x.length - 1 - suf] === w[0][w[0].length - 1 - suf])) suf++;
  return w.map((x, i) => x.slice(pre[i], x.length - suf).join(" ") || x.join(" "));
}
const HL_COLORS = ["#4469d0", "#e8b33f", "#e9735a", "#5fb7a0", "#9b6ad6", "#4fa7d8", "#c75c8a", "#7f8c3d"];
const HL_CAUSE = { local: "Heimnetz", internet: "Internet/Anbieter", unknown: "unbekannt" };

const detailCss = `
.hld{display:block;color:var(--primary-text-color)}
.hld .hld-vals{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;margin-bottom:8px}
.hld .hld-v{background:var(--card-background-color,#fff);border:1px solid var(--divider-color);border-radius:12px;padding:10px 12px;cursor:pointer;min-width:0}
.hld .hld-n{font-size:13px;color:var(--secondary-text-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hld .hld-x{font-size:17px;font-weight:500;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hld .hld-v.na .hld-x{color:var(--secondary-text-color);font-weight:400}
.hld .hld-box{background:var(--card-background-color,#fff);border:1px solid var(--divider-color);border-radius:12px;padding:12px 14px;margin-bottom:8px}
.hld .hld-t{font-size:15px;font-weight:500;margin-bottom:8px}
.hld .hld-hint{font-size:14px;line-height:1.5;color:var(--secondary-text-color)}
.hld .hld-row{display:flex;align-items:center;gap:10px;padding:5px 0;font-size:14px}.hld .hld-row .r{margin-left:auto;color:var(--secondary-text-color);text-align:right}
.hld .dot{width:12px;height:12px;border-radius:50%;flex:none}.hld .dot.ok{background:var(--hl-ok,#2e7d32)}.hld .dot.warn{background:var(--hl-warn,#f29d0b)}.hld .dot.err{background:var(--hl-err,#db4437)}.hld .dot.mut{background:var(--divider-color)}
.hld table{border-collapse:collapse;width:100%;font-size:14px}.hld td,.hld th{padding:6px 8px;border-bottom:1px solid var(--divider-color);text-align:left}.hld th{font-weight:500;color:var(--secondary-text-color)}
.hld .hld-c svg{width:100%;height:150px;display:block}
.hld .hld-ax{display:flex;justify-content:space-between;font-size:11px;color:var(--secondary-text-color);margin-top:2px}
.hld .hld-leg{display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:8px;font-size:13px}.hld .hld-leg span{cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.hld .hld-leg i{width:10px;height:10px;border-radius:50%;display:inline-block}.hld .hld-leg b{font-weight:400;color:var(--secondary-text-color)}
.hld .hld-tl{display:grid;grid-template-columns:auto 1fr;gap:6px 10px;align-items:center;font-size:13px}
.hld .hld-tl .lb{color:var(--secondary-text-color);white-space:nowrap;text-align:right;cursor:pointer}
.hld .hld-tl .bar{position:relative;height:22px;border-radius:4px;overflow:hidden;background:var(--divider-color)}
.hld .hld-tl .bar div{position:absolute;top:0;bottom:0;color:#fff;font-size:11px;line-height:22px;padding-left:4px;overflow:hidden;white-space:nowrap;box-sizing:border-box;border-right:1px solid rgba(255,255,255,.4)}
.hld .hld-empty{color:var(--secondary-text-color);font-size:13px;padding:6px 0}
.hld .hld-ctl{min-height:40px}.hld .hld-ctl ha-icon{color:var(--state-icon-color,#44739e);cursor:pointer;flex:none;width:40px;display:flex;justify-content:center}
.hld .hld-ctl .n{flex:1;min-width:0;cursor:pointer;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hld .hld-ctl .r{color:var(--primary-text-color)}
.hld .hld-sw{width:36px;height:20px;border-radius:10px;border:0;padding:0;position:relative;cursor:pointer;flex:none;margin-left:auto;background:var(--switch-unchecked-track-color,#9e9e9e)}
.hld .hld-sw::after{content:"";position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:#fff;transition:left .15s}
.hld .hld-sw.on{background:var(--switch-checked-track-color,var(--primary-color,#03a9f4))}.hld .hld-sw.on::after{left:18px}
.hld .hld-b{margin-left:auto;border:0;background:none;color:var(--primary-color,#03a9f4);font:inherit;font-weight:500;cursor:pointer;padding:6px 8px;border-radius:6px}
.hld .hld-b:hover{background:var(--secondary-background-color)}
.hld .hld-in{margin-left:auto;font:inherit;padding:4px 6px;border:1px solid var(--divider-color);border-radius:6px;background:var(--card-background-color,#fff);color:var(--primary-text-color);max-width:50%}
.hld .hld-v.warn{border-color:var(--hl-warn,#f29d0b);background:color-mix(in srgb,var(--hl-warn,#f29d0b) 14%,var(--card-background-color,#fff))}
.hld .hld-v.err{border-color:var(--hl-err,#db4437);background:color-mix(in srgb,var(--hl-err,#db4437) 10%,var(--card-background-color,#fff))}
.hld .hld-v.miss{border-style:dashed;border-color:var(--hl-err,#db4437)}
.hld .hld-hint.warn{background:color-mix(in srgb,var(--hl-warn,#f29d0b) 14%,var(--card-background-color,#fff));color:var(--primary-text-color)}
.hld .hld-hint.err{background:color-mix(in srgb,var(--hl-err,#db4437) 10%,var(--card-background-color,#fff));color:var(--primary-text-color)}
.hld .hld-stats{font-size:12px;color:var(--secondary-text-color);margin-top:6px;font-variant-numeric:tabular-nums}
.hld .hld-tools{display:flex;justify-content:flex-end;align-items:center;gap:8px;margin:-4px 0 4px;font-size:12px;color:var(--secondary-text-color)}
.hld .hld-tlv>div{border-left:2px solid var(--divider-color);padding:0 0 10px 14px;position:relative;font-size:14px;margin-left:5px}
.hld .hld-tlv>div::before{content:"";position:absolute;left:-7px;top:4px;width:12px;height:12px;border-radius:50%;background:var(--hl-ok,#2e7d32)}
.hld .hld-tlv>div.err::before{background:var(--hl-err,#db4437)}.hld .hld-tlv>div.warn::before{background:var(--hl-warn,#f29d0b)}
.hld .hld-tlv small{display:block;color:var(--secondary-text-color);font-size:12px}
.hle .hle-b{border:1.5px dashed var(--divider-color);border-radius:14px;padding:6px 8px 2px;margin-bottom:10px;background:color-mix(in srgb,var(--primary-color,#03a9f4) 3%,transparent)}
.hle .hle-b.sel{border:2px solid var(--primary-color,#03a9f4)}
.hle .hle-h{display:flex;align-items:center;gap:8px;font-size:14px;min-height:36px}.hle .hle-h ha-icon{--mdc-icon-size:18px;color:var(--secondary-text-color)}
.hle .hle-h b{font-weight:500;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hle .hle-tools{margin-left:auto;display:flex;gap:2px;flex:none}
.hle .hle-ib{width:34px;height:34px;border:0;border-radius:8px;background:none;color:var(--secondary-text-color);cursor:pointer;font:inherit;font-size:16px;flex:none}
.hle .hle-ib:hover{background:var(--secondary-background-color)}.hle .hle-ib:disabled{opacity:.3;cursor:default}
.hle .hle-ib.on{background:var(--primary-color,#03a9f4);color:#fff}
.hle .hle-miss{font-size:11px;background:var(--hl-err,#db4437);color:#fff;border-radius:9px;padding:1px 7px;flex:none}
.hle .hle-form{background:var(--card-background-color,#fff);border:1px solid var(--divider-color);border-radius:12px;padding:10px 12px;margin:4px 0 8px;display:grid;gap:10px}
.hle .hle-p{opacity:.95}
.hle .hle-p>.hld-t:first-child,.hle .hle-p>.hld-box>.hld-t:first-child{display:none}
.hle .hle-form>*,.hle .hle-f{min-width:0}
.hle .hle-f{display:grid;gap:4px;font-size:12px;color:var(--secondary-text-color)}
.hle .hle-in{font:inherit;font-size:14px;padding:7px 9px;border:1px solid var(--divider-color);border-radius:8px;background:var(--card-background-color,#fff);color:var(--primary-text-color);min-width:0;box-sizing:border-box;width:100%}
.hle .hle-in.sm{width:auto;padding:4px 6px}.hle .hle-in.num{width:76px}
.hle textarea.hle-in{resize:vertical}
.hle .hle-sub{font-size:12px;color:var(--secondary-text-color);text-transform:uppercase;letter-spacing:.05em}
.hle .hle-row{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;font-size:14px}.hle .hle-row>span:first-child{min-width:110px;color:var(--secondary-text-color)}
.hle .hle-seg{display:inline-flex;flex-wrap:wrap;background:var(--secondary-background-color);border-radius:10px;padding:3px;gap:2px}
.hle .hle-seg button{border:0;background:none;padding:5px 10px;border-radius:8px;cursor:pointer;color:var(--secondary-text-color);font:inherit;font-size:13px}
.hle .hle-seg button.on{background:var(--card-background-color,#fff);color:var(--primary-text-color);font-weight:500;box-shadow:0 1px 2px rgba(0,0,0,.15)}
.hle .hle-ents{display:grid;gap:6px}
.hle .hle-ent{display:flex;align-items:center;gap:4px;border:1px solid var(--divider-color);border-radius:10px;padding:5px 6px 5px 10px;font-size:14px}
.hle .hle-ent.miss{border-color:var(--hl-err,#db4437)}.hle .hle-ent.miss b{color:var(--hl-err,#db4437);font-weight:500}
.hle .hle-ent .n{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}.hle .hle-ent small{display:block;font-size:12px;color:var(--secondary-text-color);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hle .hle-cols{display:flex;gap:4px;margin-top:4px}.hle .hle-cols button{width:20px;height:20px;border-radius:50%;border:2px solid transparent;padding:0;cursor:pointer}
.hle .hle-cols button.on{border-color:var(--primary-text-color)}
.hle .hle-left{margin-left:0;justify-self:start;padding-left:2px}
.hle .hle-rule{display:flex;flex-wrap:wrap;align-items:center;gap:6px;border:1px solid var(--divider-color);border-radius:10px;padding:6px 8px;font-size:14px}
.hle .hle-hint{font-size:12px;color:var(--secondary-text-color)}
.hle .hle-bar{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0}
.hle .hle-add{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;margin:6px 0 10px}
.hle .hle-add button{display:flex;gap:10px;align-items:flex-start;text-align:left;border:1px solid var(--divider-color);border-radius:12px;background:var(--card-background-color,#fff);padding:10px;cursor:pointer;font:inherit;color:var(--primary-text-color)}
.hle .hle-add small{display:block;color:var(--secondary-text-color);font-size:12px}.hle .hle-add b{font-weight:500}
.hle .hle-foot{display:flex;flex-wrap:wrap;gap:6px;align-items:center;border-top:1px solid var(--divider-color);padding-top:10px;margin-top:6px}
.hle .hle-pri{border:0;border-radius:8px;background:var(--primary-color,#03a9f4);color:var(--text-primary-color,#fff);font:inherit;font-weight:500;padding:8px 16px;cursor:pointer}
.hle-ov{position:fixed;inset:0;z-index:1002;background:rgba(0,0,0,.45);display:flex;align-items:flex-start;justify-content:center;padding:6vh 10px;overflow:auto}
.hle-dlg{background:var(--card-background-color,#fff);color:var(--primary-text-color);border-radius:16px;width:min(560px,100%);padding:12px 14px 14px;display:grid;gap:8px;box-sizing:border-box}
.hle-dh{display:flex;align-items:center}.hle-dh b{flex:1;font-size:17px;font-weight:500}
.hle-chips{display:flex;flex-wrap:wrap;gap:6px}.hle-chips button{border:1px solid var(--divider-color);border-radius:16px;padding:3px 10px;background:none;cursor:pointer;font:inherit;font-size:13px;color:var(--primary-text-color)}
.hle-chips button.on{background:var(--primary-color,#03a9f4);border-color:var(--primary-color,#03a9f4);color:#fff}
.hle-list{display:grid;gap:4px;max-height:50vh;overflow:auto}
.hle-pi{display:flex;gap:8px;text-align:left;border:1px solid var(--divider-color);border-radius:10px;padding:7px 10px;background:none;cursor:pointer;font:inherit;font-size:14px;color:var(--primary-text-color)}
.hle-pi>span:first-child{flex:1;min-width:0}.hle-pi small{display:block;color:var(--secondary-text-color);font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hle-pi .r{color:var(--secondary-text-color);white-space:nowrap}.hle-pi.used{opacity:.5}`;

const HL_TOGGLE = new Set(["switch", "input_boolean", "light", "fan", "automation", "siren", "humidifier"]);
const HL_CTL_ICON = { switch: "mdi:toggle-switch-variant", input_boolean: "mdi:toggle-switch-variant", button: "mdi:gesture-tap-button",
  input_button: "mdi:gesture-tap-button", script: "mdi:script-text", time: "mdi:clock-outline", select: "mdi:format-list-bulleted",
  input_select: "mdi:format-list-bulleted", number: "mdi:ray-vertex", input_number: "mdi:ray-vertex", light: "mdi:lightbulb", sensor: "mdi:eye" };
/** Zeitpunkt wie „heute 22:42 (vor 3 Min.)“ – ohne HA-Hilfsbausteine. */
function hlWhen(h, iso) {
  const d = new Date(iso); if (isNaN(d)) return "–";
  const lang = (h && h.locale && h.locale.language) || (h && h.language) || "de";
  const now = new Date(), day = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const dd = Math.round((new Date(d.getFullYear(), d.getMonth(), d.getDate()) - day) / 864e5);
  const time = d.toLocaleTimeString(lang, { hour: "2-digit", minute: "2-digit" });
  const min = Math.round((now - d) / 6e4);
  let rel = "", date = d.toLocaleDateString(lang, { day: "2-digit", month: "2-digit", year: "numeric" });
  try { const rf = new Intl.RelativeTimeFormat(lang, { numeric: "auto" });
    if (dd === 0 || dd === -1) date = rf.format(dd, "day");   // „heute“ / „gestern“ in der Sprache des Nutzers
    rel = Math.abs(min) < 60 ? rf.format(-min, "minute") : Math.abs(min) < 1440 * 2 ? rf.format(-Math.round(min / 60), "hour") : rf.format(-Math.round(min / 1440), "day");
  } catch (e) { /* ältere Browser */ }
  return `${date} ${time}${rel ? ` (${rel})` : ""}`;
}
class HomeLinesDetail extends HTMLElement {
  set spec(v) { this._kind = undefined; this._setSpec(v); }
  set state(v) {
    this._s = v;
    if (this._edit) return;   // während der Bearbeitung nicht neu zeichnen
    if (this._kind !== undefined && !this._edit && this._spec) {
      const n = hlDetail(v, this._kind, this._wid);
      if (JSON.stringify(n.blocks) !== JSON.stringify(this._spec.blocks)) { this._setSpec(n); return; }
      this._spec.custom = n.custom;
    }
    this._paint();
  }
  set hass(h) {
    const first = !this._hass; this._hass = h;
    if (first) { this._load(); this._sub(); }
    const key = this._ents().map(e => h.states[e] && h.states[e].state).join("|");
    if (key !== this._key && !this._edit) { this._key = key; this._paint(); }
  }
  _ents() { return ((this._spec || {}).blocks || []).flatMap(b => b.entities || []); }
  _name(e) { const st = this._hass && this._hass.states[e]; return hlCleanName((st && st.attributes.friendly_name) || e); }
  _names(list) { return hlShortNames(list.map(e => this._name(e))); }
  _val(e) {
    const h = this._hass, st = h && h.states[e];
    if (!st || ["unavailable", "unknown"].includes(st.state)) return null;
    try { if (h.formatEntityState) return h.formatEntityState(st); } catch (err) { /* ältere HA */ }
    return hlFmt(h, e) ?? st.state;
  }
  async _load(blocks) {
    const sp = this._spec, h = this._hass;
    if (!sp || !h || !h.callWS) return;
    const need = {};
    (blocks || sp.blocks).filter(b => b.type === "chart" || b.type === "timeline").forEach(b => b.entities.forEach(e => { need[e] = Math.max(need[e] || 0, b.hours || 24); }));
    const byHours = {};
    Object.entries(need).forEach(([e, hrs]) => { (byHours[hrs] = byHours[hrs] || []).push(e); });
    this._series = this._series || {};
    await Promise.all(Object.entries(byHours).map(async ([hrs, ents]) => {
      try {
        const r = await h.callWS({ type: "history/history_during_period", entity_ids: ents,
          start_time: new Date(Date.now() - hrs * 3600000).toISOString(), minimal_response: true, no_attributes: true,
          significant_changes_only: false });
        ents.forEach(e => { this._series[e] = ((r && r[e]) || []).map(x => [(x.lu || x.lc || 0) * 1000, x.s]); (this._hrs = this._hrs || {})[e] = Number(hrs); });
      } catch (err) { ents.forEach(e => { this._series[e] = this._series[e] || []; (this._hrs = this._hrs || {})[e] = Number(hrs); }); }
    }));
    this._paint();
  }
  _pts(e, hrs) {
    const t1 = Date.now(), t0 = t1 - hrs * 3600000;
    const pts = ((this._series || {})[e] || []).filter(p => p[0] <= t1);
    const st = this._hass.states[e];
    if (st) pts.push([t1, st.state]);
    // Vor dem Zeitraum liegende Werte gelten ab Beginn
    return pts.map(p => [Math.max(p[0], t0), p[1]]);
  }
  _axis(hrs, t0) {
    const t1 = Date.now(), span = (t1 - t0) / 3600000;
    const from = span >= hrs - 0.5 ? (hrs >= 48 ? `vor ${Math.round(hrs / 24)} Tagen` : `vor ${hrs} Stunden`) : `seit ${when(new Date(t0).toISOString())}`;
    return `<div class="hld-ax"><span>${from}</span><span>jetzt</span></div>`;
  }
  _chart(b) {
    const h = this._hass, hrs = b.hours || 24, t1 = Date.now();
    const ents = b.entities.filter(e => h.states[e]);
    const numeric = ents.filter(e => !e.startsWith("binary_sensor.") && !isNaN(parseFloat(h.states[e].state)));
    if (!numeric.length) return "";
    // Gleiche Einheit → ein Diagramm; „je Wert eine Grafik“ → jede Entität einzeln
    const groups = {};
    numeric.forEach(e => { const k = b.mode === "separate" ? e : (h.states[e].attributes.unit_of_measurement || ""); (groups[k] = groups[k] || []).push(e); });
    const color = e => (b.colors && HL_NAMED[b.colors[e]]) || HL_COLORS[numeric.indexOf(e) % HL_COLORS.length];
    const lv = b.limit && b.limit.on ? parseFloat(String(b.limit.v).replace(",", ".")) : NaN;
    const lim = isNaN(lv) ? null : lv, limCol = b.limit && b.limit.c === "err" ? "var(--hl-err,#db4437)" : "var(--hl-warn,#f29d0b)";
    const beyond = v => lim != null && (b.limit.dir === "above" ? v > lim : v < lim);
    const valAt = (pts, t) => { let v = null; for (const p of pts) { if (p[0] <= t) v = p[1]; else break; } return v; };
    return Object.entries(groups).map(([, list]) => {
      const u = h.states[list[0]].attributes.unit_of_measurement || "";
      const series = list.map(e => this._pts(e, hrs).map(p => [p[0], parseFloat(p[1])]).filter(p => !isNaN(p[1])));
      const first = Math.min(...series.map(s => (s[0] || [t1])[0]));
      const t0 = b.kind === "bar" ? t1 - hrs * 3600000 : Math.min(t1 - 600000, Math.max(t1 - hrs * 3600000, first));
      const all = series.flat().map(p => p[1]); if (lim != null) all.push(lim);
      let lo = Math.min(...all), hi = Math.max(...all);
      if ((lo > 0 && lo < hi - lo) || b.kind === "bar" || b.kind === "area") lo = Math.min(0, lo);
      if (!isFinite(lo) || !isFinite(hi)) return "";
      if (hi - lo < 1e-9) { if (lo === 0) hi = 1; else { lo -= Math.abs(lo) * 0.1 || 1; hi += Math.abs(hi) * 0.1 || 1; } }
      const X = t => (t - t0) / (t1 - t0) * 100, Y = v => 96 - (v - lo) / (hi - lo) * 92;
      let paths = "";
      if (lim != null) {
        const y = Y(lim);
        paths += b.limit.dir === "above" ? `<rect x="0" y="0" width="100" height="${y.toFixed(2)}" fill="${limCol}" opacity=".08"/>`
          : `<rect x="0" y="${y.toFixed(2)}" width="100" height="${(100 - y).toFixed(2)}" fill="${limCol}" opacity=".08"/>`;
        paths += `<line x1="0" x2="100" y1="${y.toFixed(2)}" y2="${y.toFixed(2)}" stroke="${limCol}" stroke-width="1.2" stroke-dasharray="4 3" vector-effect="non-scaling-stroke"/>`;
      }
      if (b.kind === "bar") {
        const n = hrs <= 24 ? 24 : hrs <= 168 ? 28 : 30, bw = 100 / n, w = bw * 0.8 / list.length, base = Y(Math.max(lo, 0));
        series.forEach((pts, i) => {
          for (let k = 0; k < n; k++) {
            const a = t0 + k * (t1 - t0) / n, z = a + (t1 - t0) / n;
            const s = [0, 1, 2, 3, 4, 5].map(j => valAt(pts, a + (j + 0.5) * (z - a) / 6)).filter(v => v != null);
            if (!s.length) continue;
            const v = s.reduce((x, y) => x + y, 0) / s.length, y = Y(v);
            paths += `<rect x="${(k * bw + bw * 0.1 + i * w).toFixed(2)}" y="${Math.min(y, base).toFixed(2)}" width="${w.toFixed(2)}" height="${Math.abs(base - y).toFixed(2)}" fill="${beyond(v) ? limCol : color(list[i])}"/>`;
          }
        });
      } else {
        paths += series.map((pts, i) => {
          // Stufenverlauf; je ~0,25 % Breite höchstens ein Minimum und ein Maximum (Spitzen bleiben sichtbar)
          let d = "", lastX = -1, lastY = null, mn = null, mx = null, x0 = 0;
          const flush = x => { if (mn == null) return; d += ` L${x.toFixed(2)},${Y(mn).toFixed(2)} L${x.toFixed(2)},${Y(mx).toFixed(2)}`; };
          pts.forEach((p, k) => {
            const x = X(p[0]);
            if (k === 0) { d = `M${x.toFixed(2)},${Y(p[1]).toFixed(2)}`; lastX = x0 = x; lastY = p[1]; return; }
            if (x - lastX < 0.25) { mn = Math.min(mn ?? p[1], p[1]); mx = Math.max(mx ?? p[1], p[1]); lastY = p[1]; return; }
            flush(lastX); mn = mx = null;
            d += ` L${x.toFixed(2)},${Y(lastY).toFixed(2)} L${x.toFixed(2)},${Y(p[1]).toFixed(2)}`; lastX = x; lastY = p[1];
          });
          if (!d) return "";
          flush(lastX); d += ` L100,${Y(lastY ?? 0).toFixed(2)}`;
          const fill = b.kind === "area" ? `<path d="${d} L100,${Y(Math.max(lo, 0)).toFixed(2)} L${x0.toFixed(2)},${Y(Math.max(lo, 0)).toFixed(2)} Z" fill="${color(list[i])}" opacity=".16"/>` : "";
          return `${fill}<path d="${d}" fill="none" stroke="${color(list[i])}" stroke-width="1.6" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>`;
        }).join("");
      }
      const f = v => hlNum(v, u);
      const names = this._names(list);
      const span = hrs >= 48 ? Math.round(hrs / 24) + " Tage" : hrs + " Stunden";
      const multi = Object.keys(groups).length > 1;
      const title = b.title && !multi ? b.title : list.length === 1 && multi ? `${b.title ? b.title + ": " : ""}${this._name(list[0])} – ${span}` : `${multi ? u || "Werte" : "Verlauf"} – ${span}`;
      // Min, Max und Ø (zeitlich gewichtet) über den Zeitraum
      const stats = b.stats ? list.map((e, i) => {
        const pts = series[i]; if (!pts.length) return "";
        let sum = 0, dur = 0;
        pts.forEach((p, k) => { const z = k + 1 < pts.length ? pts[k + 1][0] : t1, dt = Math.max(0, z - Math.max(p[0], t0)); sum += p[1] * dt; dur += dt; });
        const vals = pts.map(p => p[1]);
        return `<div>${list.length > 1 ? `${esc(names[i])}: ` : ""}Min ${esc(f(Math.min(...vals)))} · Max ${esc(f(Math.max(...vals)))} · Ø ${esc(f(dur ? sum / dur : vals[0]))}</div>`;
      }).join("") : "";
      return `<div class="hld-box hld-c"><div class="hld-t">${esc(title)}</div>
        <div style="display:flex;justify-content:space-between;font-size:11px;color:var(--secondary-text-color)"><span>${esc(f(hi))}</span>${lim != null ? `<span style="color:${limCol}">Grenze ${esc(f(lim))}</span>` : ""}</div>
        <svg viewBox="0 0 100 100" preserveAspectRatio="none">${paths}</svg>
        <div style="font-size:11px;color:var(--secondary-text-color)">${esc(f(lo))}</div>${this._axis(hrs, t0)}
        <div class="hld-leg">${list.map((e, i) => `<span data-e="${esc(e)}"><i style="background:${color(e)}"></i>${esc(names[i])} <b>${esc(this._val(e) ?? "–")}</b></span>`).join("")}</div>
        ${stats ? `<div class="hld-stats">${stats}</div>` : ""}</div>`;
    }).join("");
  }
  _timeline(b) {
    const h = this._hass, hrs = b.hours || 24, t1 = Date.now();
    const ents = b.entities.filter(e => h.states[e]);
    if (!ents.length) return "";
    const series = ents.map(e => this._pts(e, hrs));
    const first = Math.min(...series.map(s => (s[0] || [t1])[0]));
    const t0 = Math.min(t1 - 600000, Math.max(t1 - hrs * 3600000, first));
    const names = this._names(ents);
    const palette = {};
    const col = (e, v) => {
      if (["on", "connected", "online", "normal"].includes(v)) return "var(--hl-ok,#2e7d32)";
      if (["off", "disconnected", "offline", "emergency"].includes(v)) return "var(--hl-err,#db4437)";
      if (["unavailable", "unknown"].includes(v)) return "var(--divider-color)";
      if (v === "dayflat") return "var(--hl-warn,#f29d0b)";
      if (!(v in palette)) palette[v] = HL_COLORS[Object.keys(palette).length % HL_COLORS.length];
      return palette[v];
    };
    const label = (e, v) => { try { return h.formatEntityState ? h.formatEntityState({ ...h.states[e], state: v }) : v; } catch (err) { return v; } };
    const rows = ents.map((e, i) => {
      // gleiche Zustände hintereinander zusammenfassen
      const pts = series[i].filter((p, k, arr) => k === 0 || arr[k - 1][1] !== p[1]);
      const segs = pts.map((p, k) => {
        const a = Math.max(p[0], t0), z = k + 1 < pts.length ? pts[k + 1][0] : t1;
        if (z <= a) return "";
        const l = (a - t0) / (t1 - t0) * 100, w = (z - a) / (t1 - t0) * 100;
        return `<div style="left:${l.toFixed(2)}%;width:${w.toFixed(2)}%;background:${col(e, p[1])}" title="${esc(label(e, p[1]))}">${w > 12 ? esc(label(e, p[1])) : ""}</div>`;
      }).join("");
      return `<span class="lb" data-e="${esc(e)}">${esc(names[i])}</span><div class="bar">${segs}</div>`;
    }).join("");
    return `<div class="hld-box"><div class="hld-t">${esc(b.title || "Verlauf")}</div><div class="hld-tl">${rows}</div>${this._axis(hrs, t0)}</div>`;
  }
  _phone() {
    const s = this._s || {}, ph = s.phone || {}, mode = s.mode;
    if (!ph.configured) return "";
    const dot = c => `<span class="dot ${c}"></span>`, rows = [];
    const a = agoMin(ph.last_seen);
    rows.push([ph.reporting ? "ok" : "err", ph.reporting ? "meldet sich" : "meldet sich nicht", a != null ? `vor ${a} min` : ""]);
    if (ph.charger !== null) rows.push([ph.usb ? "ok" : (mode === "normal" ? "warn" : "err"), ph.usb ? "USB-Kabel zum Notfall-Router" : "USB-Kabel zum Notfall-Router fehlt", ph.battery != null ? Math.round(ph.battery) + " %" : ""]);
    if (ph.operator || ph.network) rows.push([ph.signal != null || ph.network ? "ok" : "warn", `Mobilfunk ${ph.operator || ""}`.trim(), [ph.network, ph.signal != null ? ph.signal + " dBm" : null].filter(Boolean).join(" · ")]);
    if (ph.mobile_data !== null) rows.push([mode === "normal" ? (ph.mobile_data ? "warn" : "ok") : (ph.mobile_data ? "ok" : "err"),
      ph.mobile_data ? "Mobile Daten an" : "Mobile Daten aus", mode === "normal" ? "im Notbetrieb an" : ""]);
    if (ph.wifi !== null && ph.wifi !== undefined) rows.push([mode === "normal" ? (ph.wifi ? "ok" : "warn") : (ph.wifi ? "warn" : "ok"),
      ph.wifi ? "WLAN verbunden" : "WLAN aus", ph.wifi_name && ph.wifi ? ph.wifi_name : ""]);
    return `<div class="hld-box"><div class="hld-t">Notfall-Handy</div>${rows.map(r => `<div class="hld-row">${dot(r[0])}<span>${esc(r[1])}</span><span class="r">${esc(r[2])}</span></div>`).join("")}</div>`;
  }
  _log(b = {}) {
    const s = this._s || {}, h = this._hass, n = b.n || 20, src = b.src || "outages";
    const title = b.title || (src === "switch" ? "Notbetrieb" : src === "reconnect" ? "Neueinwahl" : "Protokoll");
    const box = inner => `<div class="hld-box"><div class="hld-t">${esc(title)}</div>${inner}</div>`;
    let rows = [];
    if (src === "outages") {
      const rec = (s.monitor || {}).recent || [];
      if (b.style !== "timeline") {
        if (!rec.length) return box(`<div class="hld-empty">Keine Ausfälle aufgezeichnet.</div>`);
        return box(`<table><tr><th></th><th>Beginn</th><th>Dauer</th><th>Ursache</th></tr>
          ${rec.slice(0, n).map(o => `<tr><td><span class="dot ${o.cause === "internet" ? "err" : "warn"}"></span></td><td>${esc(o.start)}</td><td>${esc(o.duration)}</td><td>${esc(HL_CAUSE[o.cause] || o.cause || "")}</td></tr>`).join("")}</table>`);
      }
      rows = rec.slice(0, n).map(o => [o.cause === "internet" ? "err" : "warn", o.start, `${o.duration} · ${HL_CAUSE[o.cause] || o.cause || ""}`]);
    } else if (src === "switch") {
      rows = (s.emergencies || []).slice().reverse().slice(0, n).map(x => ["err", hlWhen(h, x.start),
        `Notbetrieb bis ${x.end ? hlWhen(h, x.end) : "jetzt"}${x.flat ? " · mit Tagesflat" : ""}`]);
    } else if (src === "reconnect") {
      const r = s.reconnect || {};
      if (r.last) rows = [[r.error ? "err" : "ok", hlWhen(h, r.last), [r.result, r.ip].filter(Boolean).join(" · ") || "–"]];
    }
    if (!rows.length) return box(`<div class="hld-empty">Noch keine Einträge.</div>`);
    if (b.style === "timeline") return box(`<div class="hld-tlv">${rows.map(([c, t, d]) => `<div class="${c}"><small>${esc(t)}</small>${esc(d)}</div>`).join("")}</div>`);
    return box(rows.map(([c, t, d]) => `<div class="hld-row"><span class="dot ${c}"></span><span>${esc(d)}</span><span class="r">${esc(t)}</span></div>`).join(""));
  }
  /* Bedienzeilen (Schalter, Knöpfe, Uhrzeit, Auswahl, Zahl, Zeitpunkt) zeichnet HomeLines selbst.
     Die HA-Liste („entities“) bleibt in diesem Fenster seit HA 2026 teils leer: Schalter und Zeitangaben holen
     sich ihre Daten dort aus der HA-Oberfläche, und unser Fenster liegt außerhalb davon. */
  _controls(b) {
    const h = this._hass, names = this._names(b.entities);
    const rows = b.entities.map((e, k) => {
      const st = h.states[e], dom = e.split(".")[0], na = !st || st.state === "unavailable";
      const icon = (st && st.attributes.icon) || HL_CTL_ICON[dom] || "mdi:information-outline";
      let right;
      if (na) right = `<span class="r">nicht verfügbar</span>`;
      else if (HL_TOGGLE.has(dom)) right = `<button class="hld-sw${st.state === "on" ? " on" : ""}" data-act="toggle" data-x="${esc(e)}" role="switch" aria-checked="${st.state === "on"}" aria-label="${esc(names[k])}"></button>`;
      else if (dom === "button" || dom === "input_button") right = `<button class="hld-b" data-act="press" data-x="${esc(e)}">Drücken</button>`;
      else if (dom === "script") right = `<button class="hld-b" data-act="run" data-x="${esc(e)}">Ausführen</button>`;
      else if (dom === "time") right = `<input class="hld-in" type="time" step="60" data-act="time" data-x="${esc(e)}" value="${esc(String(st.state).slice(0, 5))}">`;
      else if ((dom === "select" || dom === "input_select") && Array.isArray(st.attributes.options))
        right = `<select class="hld-in" data-act="select" data-x="${esc(e)}">${st.attributes.options.map(o => `<option${o === st.state ? " selected" : ""}>${esc(o)}</option>`).join("")}</select>`;
      else if (dom === "number" || dom === "input_number")
        right = `<input class="hld-in" type="number" data-act="number" data-x="${esc(e)}" value="${esc(st.state)}" min="${esc(st.attributes.min ?? "")}" max="${esc(st.attributes.max ?? "")}" step="${esc(st.attributes.step ?? "any")}">`;
      else if (st.attributes.device_class === "timestamp") right = `<span class="r">${esc(hlWhen(h, st.state))}</span>`;
      else right = `<span class="r">${esc(this._val(e) ?? "–")}</span>`;
      return `<div class="hld-row hld-ctl"><ha-icon icon="${esc(icon)}" data-e="${esc(e)}"></ha-icon><span class="n" data-e="${esc(e)}">${esc(names[k])}</span>${right}</div>`;
    });
    return `<div class="hld-box">${b.title ? `<div class="hld-t">${esc(b.title)}</div>` : ""}${rows.join("") || `<div class="hld-empty">–</div>`}</div>`;
  }
  _act(el, ev) {
    const h = this._hass, e = el.dataset.x, dom = e.split(".")[0], a = el.dataset.act;
    if (!h || !h.callService) return;
    if (a === "toggle") { const st = h.states[e]; return h.callService(dom, st && st.state === "on" ? "turn_off" : "turn_on", { entity_id: e }); }
    if (a === "press") return h.callService(dom, "press", { entity_id: e });
    if (a === "run") return h.callService("script", "turn_on", { entity_id: e });
    if (ev.type !== "change") return;
    if (a === "time" && el.value) return h.callService("time", "set_value", { entity_id: e, time: `${el.value}:00` });
    if (a === "select") return h.callService(dom, "select_option", { entity_id: e, option: el.value });
    if (a === "number" && el.value !== "") return h.callService(dom, "set_value", { entity_id: e, value: Number(el.value) });
  }
  /* ---------------------------------------------------------------- ab 0.9.0: Fenster öffnen, anpassen, speichern */
  open(s, kind, wid) { this._kind = kind; this._wid = wid; if (s) this._s = s; this._setSpec(hlDetail(this._s || {}, kind, wid)); this._sub(); }
  _setSpec(v) { this._spec = v; this._series = null; this._hrs = {}; this._key = null; this._root = null; this._slots = null; this.innerHTML = ""; this._paint(); this._load(); }
  connectedCallback() { this._sub(); }
  disconnectedCallback() { if (this._feed) { this._feed.remove(this._fl); this._feed = null; } }
  _sub() {
    if (this._kind === undefined || this._feed || !this._hass || !this._hass.connection || !this.isConnected) return;
    this._fl = f => { if (f.data && f.data !== this._s) this.state = f.data; };
    this._feed = hlFeed(this._hass, (this._s || {}).entry_id); this._feed.add(this._fl);
  }
  _admin() { const u = this._hass && this._hass.user; return !!(u && u.is_admin) && this._kind !== undefined; }
  _bind() {
    if (this._bound) return; this._bound = true;
    this.addEventListener("click", ev => {
      const ed = ev.target.closest("[data-ed]"); if (ed) { this._edClick(ed, ev); return; }
      if (this._edit) return;
      const c = ev.target.closest("[data-act]"); if (c) { if (c.tagName === "BUTTON") this._act(c, ev); return; }
      const t = ev.target.closest("[data-e]"); if (t) hlMoreInfo(t.dataset.e); });
    this.addEventListener("change", ev => {
      const f = ev.target.closest("[data-f]"); if (f && this._edit) { this._edSet(f.dataset.f, f.value, f.dataset.i); return; }
      const c = ev.target.closest("[data-act]"); if (c && !this._edit) this._act(c, ev); });
    this.addEventListener("input", ev => {
      if (ev.target.dataset.pq !== undefined && this._edit && this._edit.pick) { this._edit.pick.q = ev.target.value; this._paintPick(); }
    });
  }
  _startEdit() { this._edit = { draft: hlToStored(this._spec.blocks), sel: null, add: false, pick: null, err: "" }; this._paint(); }
  _cur() { return this._edit.draft[this._edit.sel]; }
  _edSet(path, val, i) {
    const E = this._edit, b = E.draft[i != null ? Number(i) : E.sel]; if (!b) return;
    const ks = path.split("."); let o = b;
    ks.slice(0, -1).forEach(k => { o = o[k]; });
    const last = ks[ks.length - 1];
    o[last] = typeof o[last] === "number" ? Number(val) : val;
    this._paint();
  }
  async _save(reset) {
    const E = this._edit, msg = { type: "homelines/set_windows", key: this._spec.key };
    if (!reset) msg.blocks = E.draft;
    if (this._s && this._s.entry_id) msg.entry_id = this._s.entry_id;
    try {
      const w = await this._hass.callWS(msg);
      this._s = { ...(this._s || {}), windows: w }; this._edit = null;
      this._setSpec(hlDetail(this._s, this._kind, this._wid));
    } catch (e) { E.err = `Speichern ging nicht: ${e.message || e}`; this._paint(); }
  }
  _edClick(el, ev) {
    const a = el.dataset.ed, E = this._edit, i = el.dataset.i != null ? Number(el.dataset.i) : null;
    if (a === "start") return this._startEdit();
    if (!E) return;
    const d = E.draft;
    if (a === "cancel") { this._edit = null; this._setSpec(hlDetail(this._s || {}, this._kind, this._wid)); return; }
    if (a === "save") return this._save(false);
    if (a === "reset") return this._save(true);
    if (a === "sel") E.sel = E.sel === i ? null : i;
    else if (a === "up" || a === "down") { const j = a === "up" ? i - 1 : i + 1; if (j < 0 || j >= d.length) return; [d[i], d[j]] = [d[j], d[i]]; if (E.sel === i) E.sel = j; }
    else if (a === "rm") { d.splice(i, 1); E.sel = null; }
    else if (a === "addopen") E.add = !E.add;
    else if (a === "add") {
      const t = el.dataset.v;
      const nb = { values: { t, title: "Werte", ents: [], rules: [], style: "tiles" },
        chart: { t, title: "Grafik", ents: [], kind: "line", range: "24h", mode: "together", colors: {}, limit: HL_NOLIMIT(), stats: false },
        actions: { t, title: "Bedienung", ents: [] }, log: { t, title: "Protokoll", src: "outages", n: 5, style: "timeline" },
        text: { t, text: "", tone: "info" }, phone: { t, title: "" } }[t];
      d.push(nb); E.add = false; E.sel = d.length - 1;
    }
    else if (a === "fritz") { const f = hlFritzTemplate(this._hass); if (!f.length) { E.err = "Keine FRITZ!Box-Werte gefunden (Integrationen FRITZ!Box Tools, FRITZ!SmartHome oder Ping)."; } else { E.draft = d.concat(f); E.sel = null; E.err = ""; } }
    else if (a === "setv") { this._edSet(el.dataset.f, el.dataset.v, el.dataset.bi); return; }
    else if (a === "flip") { const b = d[Number(el.dataset.bi)], ks = el.dataset.f.split("."); let o = b; ks.slice(0, -1).forEach(k => { o = o[k]; }); o[ks[ks.length - 1]] = !o[ks[ks.length - 1]]; }
    else if (a === "erm") { const b = d[Number(el.dataset.bi)]; const e = b.ents.splice(i, 1)[0]; if (b.colors) delete b.colors[e]; }
    else if (a === "eup" || a === "edown") { const l = d[Number(el.dataset.bi)].ents, j = a === "eup" ? i - 1 : i + 1; if (j < 0 || j >= l.length) return; [l[i], l[j]] = [l[j], l[i]]; }
    else if (a === "color") { const b = d[Number(el.dataset.bi)]; b.colors = { ...(b.colors || {}), [el.dataset.e]: el.dataset.v }; }
    else if (a === "radd") d[Number(el.dataset.bi)].rules.push({ c: "warn", any: "any", grp: "all", when: "unavail", v: "" });
    else if (a === "rrm") d[Number(el.dataset.bi)].rules.splice(i, 1);
    else if (a === "pick") { E.pick = { bi: Number(el.dataset.bi), rep: i, q: "", area: "", tab: "sug" }; }
    else if (a === "ptab") { E.pick.tab = el.dataset.v; this._paintPick(); return; }
    else if (a === "parea") { E.pick.area = el.dataset.v; this._paintPick(); return; }
    else if (a === "pclose") { if (el.dataset.self && ev.target !== el) return; E.pick = null; }
    else if (a === "choose") {
      const P = E.pick, l = d[P.bi].ents, e = el.dataset.v;
      if (P.rep != null) l[P.rep] = e; else if (!l.includes(e)) l.push(e);
      E.pick = null;
    }
    else return;
    this._paint();
  }
  /* Auswahl von Entitäten: eigene Liste (HAs Auswahl braucht die HA-Oberfläche, unser Fenster liegt außerhalb) */
  _area(e) {
    const h = this._hass, r = (h.entities || {})[e]; if (!r) return "";
    const id = r.area_id || (r.device_id && h.devices && h.devices[r.device_id] && h.devices[r.device_id].area_id);
    return (id && h.areas && h.areas[id] && h.areas[id].name) || "";
  }
  _fits(b, e) {
    const h = this._hass, st = h.states[e], dom = e.split(".")[0];
    if (b.t === "chart") return b.kind === "strip" ? ["binary_sensor", "switch", "input_boolean"].includes(dom) || !isNaN(parseFloat(st.state)) === false
      : !isNaN(parseFloat(st.state)) && dom !== "binary_sensor";
    if (b.t === "actions") return HL_CTL.test(e) || ["switch", "input_boolean", "light", "time", "select", "number"].includes(dom) || st.attributes.device_class === "timestamp";
    const have = (b.ents || []).filter(x => h.states[x]);
    if (!have.length) return true;
    const g = new Set(have.map(x => hlGrp(h, x)));
    return g.has(hlGrp(h, e)) || have.some(x => x.split(".")[0] === dom && (h.states[x].attributes.unit_of_measurement || "") === (st.attributes.unit_of_measurement || "") && (st.attributes.unit_of_measurement || ""));
  }
  _pickHtml() {
    const E = this._edit, P = E.pick, h = this._hass, b = E.draft[P.bi];
    const all = Object.keys(h.states).filter(e => !e.startsWith("update.") || b.t === "values").sort();
    const sug = all.filter(e => this._fits(b, e));
    let list = P.tab === "sug" ? sug : all;
    // gleiche Einheit wie die schon gewählten Werte zuerst
    const units = new Set((b.ents || []).filter(e => h.states[e]).map(e => h.states[e].attributes.unit_of_measurement || ""));
    if (units.size) list = [...list].sort((x, y) => (units.has(h.states[y].attributes.unit_of_measurement || "") ? 1 : 0) - (units.has(h.states[x].attributes.unit_of_measurement || "") ? 1 : 0));
    const areas = [...new Set(list.map(e => this._area(e)).filter(Boolean))].sort((x, y) => x.localeCompare(y, "de"));
    if (P.area) list = list.filter(e => this._area(e) === P.area);
    const q = (P.q || "").toLowerCase().trim();
    if (q) list = list.filter(e => e.includes(q) || this._name(e).toLowerCase().includes(q) || this._area(e).toLowerCase().includes(q));
    const cur = b.ents || [], more = list.length > 150;
    return `<div class="hle-ov" data-ed="pclose" data-self="1"><div class="hle-dlg" role="dialog" aria-label="Entität wählen">
      <div class="hle-dh"><b>${P.rep != null ? "Fehlenden Wert ersetzen" : "Entität wählen"}</b><button class="hle-ib" data-ed="pclose" aria-label="Schließen">✕</button></div>
      ${P.rep != null ? `<div class="hld-box hld-hint err">Bisher: ${esc(cur[P.rep])} – gibt es nicht mehr.</div>` : ""}
      <div class="hle-seg"><button class="${P.tab === "sug" ? "on" : ""}" data-ed="ptab" data-v="sug">Vorschläge (${sug.length})</button><button class="${P.tab === "all" ? "on" : ""}" data-ed="ptab" data-v="all">Alle (${all.length})</button></div>
      <input class="hle-in" data-pq placeholder="Suchen: Name, Bereich oder Teil der ID" value="${esc(P.q || "")}" aria-label="Suchen">
      ${areas.length ? `<div class="hle-chips"><button class="${!P.area ? "on" : ""}" data-ed="parea" data-v="">Alle Bereiche</button>${areas.map(a => `<button class="${P.area === a ? "on" : ""}" data-ed="parea" data-v="${esc(a)}">${esc(a)}</button>`).join("")}</div>` : ""}
      <div class="hle-list">${list.slice(0, 150).map(e => `<button class="hle-pi${cur.includes(e) ? " used" : ""}" data-ed="choose" data-v="${esc(e)}"><span><span>${esc(this._name(e))}</span><small>${esc(this._area(e) || "ohne Bereich")} · ${esc(e)}</small></span><span class="r">${esc(this._val(e) ?? "–")}</span></button>`).join("") || `<div class="hld-empty">Nichts gefunden.</div>`}
      ${more ? `<div class="hld-empty">Weitere ${list.length - 150} – bitte die Suche nutzen.</div>` : ""}</div></div></div>`;
  }
  _paintPick() {
    const host = this.querySelector(".hle-pickhost"); if (!host) return;
    const had = this.querySelector("[data-pq]"), pos = had ? had.selectionStart : null;
    host.innerHTML = this._edit.pick ? this._pickHtml() : "";
    const inp = this.querySelector("[data-pq]"); if (inp) { inp.focus(); if (pos != null) inp.setSelectionRange(pos, pos); }
  }
  _seg(bi, f, opts, cur) {
    return `<span class="hle-seg">${opts.map(([k, n]) => `<button class="${String(cur) === String(k) ? "on" : ""}" data-ed="setv" data-bi="${bi}" data-f="${f}" data-v="${k}">${esc(n)}</button>`).join("")}</span>`;
  }
  _sel(bi, f, opts, cur, label) {
    return `<select class="hle-in sm" data-f="${f}" data-i="${bi}" aria-label="${esc(label || f)}">${opts.map(([k, n]) => `<option value="${esc(k)}"${String(k) === String(cur) ? " selected" : ""}>${esc(n)}</option>`).join("")}</select>`;
  }
  _sw(bi, f, on, label) { return `<button class="hld-sw${on ? " on" : ""}" data-ed="flip" data-bi="${bi}" data-f="${f}" role="switch" aria-checked="${!!on}" aria-label="${esc(label)}" style="margin-left:0"></button>`; }
  _entsForm(bi, b, colors) {
    const h = this._hass;
    return `<div class="hle-ents">${b.ents.map((e, k) => {
      const miss = !h.states[e];
      const cols = colors && !miss ? `<span class="hle-cols">${Object.keys(HL_NAMED).map(c => `<button class="${(b.colors[e] || Object.keys(HL_NAMED)[k % 8]) === c ? "on" : ""}" style="background:${HL_NAMED[c]}" data-ed="color" data-bi="${bi}" data-e="${esc(e)}" data-v="${c}" aria-label="${HL_COLOR_N[c]}"></button>`).join("")}</span>` : "";
      return `<div class="hle-ent${miss ? " miss" : ""}"><span class="n">${miss ? `<b>Wert fehlt – neu wählen</b><small>${esc(e)} gibt es nicht mehr</small>` : `${esc(this._name(e))}<small>${esc(this._area(e) ? this._area(e) + " · " : "")}${esc(this._val(e) ?? "nicht verfügbar")}</small>`}${cols}</span>
        ${miss ? `<button class="hld-b" data-ed="pick" data-bi="${bi}" data-i="${k}">neu wählen</button>` : `<button class="hle-ib" data-ed="eup" data-bi="${bi}" data-i="${k}" ${k === 0 ? "disabled" : ""} aria-label="nach oben">↑</button><button class="hle-ib" data-ed="edown" data-bi="${bi}" data-i="${k}" ${k === b.ents.length - 1 ? "disabled" : ""} aria-label="nach unten">↓</button>`}
        <button class="hle-ib" data-ed="erm" data-bi="${bi}" data-i="${k}" aria-label="entfernen">✕</button></div>`; }).join("")}</div>
      <button class="hld-b hle-left" data-ed="pick" data-bi="${bi}">+ Entität hinzufügen</button>`;
  }
  _rulesForm(bi, b) {
    const h = this._hass, grps = ["all", ...new Set(b.ents.filter(e => h.states[e]).map(e => hlGrp(h, e)).filter(g => HL_GRP_N[g]))];
    return `${b.rules.map((r, k) => `<div class="hle-rule"><span class="dot ${r.c}"></span>
        ${this._sel(bi, `rules.${k}.c`, [["warn", "Gelb"], ["err", "Rot"]], r.c, "Farbe")}<span>wenn</span>
        ${this._sel(bi, `rules.${k}.any`, [["any", "ein/e"], ["all", "alle"]], r.any, "eine oder alle")}
        ${grps.length > 1 ? this._sel(bi, `rules.${k}.grp`, grps.map(g => [g, HL_GRP_N[g]]), r.grp, "Art") : "<span>Wert</span>"}
        ${this._sel(bi, `rules.${k}.when`, HL_WHEN_N, r.when, "Bedingung")}
        ${r.when !== "unavail" ? `<input class="hle-in sm num" data-f="rules.${k}.v" data-i="${bi}" value="${esc(r.v)}" aria-label="Vergleichswert">` : ""}
        <button class="hle-ib" data-ed="rrm" data-bi="${bi}" data-i="${k}" aria-label="Warnfarbe entfernen">✕</button></div>`).join("")}
      <button class="hld-b hle-left" data-ed="radd" data-bi="${bi}">+ Warnfarbe</button>
      <div class="hle-hint">Rot hat Vorrang vor Gelb.</div>`;
  }
  _form(bi) {
    const b = this._edit.draft[bi], title = b.t === "text" || b.t === "phone" ? "" :
      `<label class="hle-f">Überschrift<input class="hle-in" data-f="title" data-i="${bi}" value="${esc(b.title || "")}"></label>`;
    if (b.t === "values") return `${title}<div class="hle-sub">Werte</div>${this._entsForm(bi, b)}
      <div class="hle-row"><span>Darstellung</span>${this._seg(bi, "style", [["tiles", "Kacheln"], ["list", "Liste"]], b.style)}</div>
      <div class="hle-sub">Warnfarben je Wert</div>${this._rulesForm(bi, b)}`;
    if (b.t === "chart") return `${title}
      <div class="hle-row"><span>Art</span>${this._seg(bi, "kind", HL_KIND_N, b.kind)}</div>
      <div class="hle-row"><span>Zeitraum</span>${this._seg(bi, "range", HL_RANGE_N, b.range)}</div>
      ${b.kind !== "strip" ? `<div class="hle-row"><span>Mehrere Werte</span>${this._seg(bi, "mode", [["together", "zusammen"], ["separate", "je Wert eine Grafik"]], b.mode)}</div>` : ""}
      <div class="hle-sub">Werte${b.kind !== "strip" ? " und Farben" : ""}</div>${this._entsForm(bi, b, b.kind !== "strip")}
      ${b.kind !== "strip" ? `<div class="hle-sub">Grenzlinie</div><div class="hle-rule">${this._sw(bi, "limit.on", b.limit.on, "Grenzlinie")}<span>Linie bei</span>
        <input class="hle-in sm num" data-f="limit.v" data-i="${bi}" value="${esc(b.limit.v)}" aria-label="Grenzwert"><span>– Bereich</span>
        ${this._sel(bi, "limit.dir", [["below", "darunter"], ["above", "darüber"]], b.limit.dir, "Richtung")}${this._sel(bi, "limit.c", [["warn", "gelb"], ["err", "rot"]], b.limit.c, "Farbe")}</div>
        <div class="hle-row"><span>Min, Max und Ø zeigen</span>${this._sw(bi, "stats", b.stats, "Min Max Durchschnitt")}</div>` : `<div class="hle-hint">Grün = an/online, Rot = aus/offline.</div>`}`;
    if (b.t === "actions") return `${title}<div class="hle-sub">Bedienelemente</div>${this._entsForm(bi, b)}
      <div class="hle-hint">HomeLines zeichnet passend: Schalter, Uhrzeit, „Drücken“, Auswahl, Zahl oder Zeitpunkt.</div>`;
    if (b.t === "log") return `${title}<div class="hle-row"><span>Was</span>${this._sel(bi, "src", HL_LOG_N, b.src, "Quelle")}</div>
      <div class="hle-row"><span>Einträge</span>${this._sel(bi, "n", [[3, "3"], [5, "5"], [10, "10"], [20, "20"]], b.n, "Anzahl")}</div>
      <div class="hle-row"><span>Darstellung</span>${this._seg(bi, "style", [["timeline", "Zeitleiste"], ["list", "Liste"]], b.style)}</div>`;
    if (b.t === "text") return `<label class="hle-f">Text<textarea class="hle-in" data-f="text" data-i="${bi}" rows="3">${esc(b.text)}</textarea></label>
      <div class="hle-row"><span>Farbe</span>${this._seg(bi, "tone", [["info", "neutral"], ["warn", "gelb"], ["err", "rot"]], b.tone)}</div>`;
    return `<div class="hle-hint">Eingebaut: zeigt Kabel, Mobilfunk und mobile Daten des Notfall-Handys. Keine Einstellungen.</div>`;
  }
  _paintEdit() {
    const E = this._edit, d = E.draft, sp = hlFromStored(d);
    const have = this._hrs || {}, miss = sp.filter(b => b.type === "chart" || b.type === "timeline").some(b => b.entities.some(e => (have[e] || 0) < (b.hours || 24)));
    if (miss && !this._loading) { this._loading = true; this._load(sp).finally(() => { this._loading = false; }); }
    const blocks = d.map((b, i) => {
      const miss = (b.ents || []).filter(e => !this._hass.states[e]).length;
      return `<div class="hle-b${E.sel === i ? " sel" : ""}">
        <div class="hle-h"><ha-icon icon="${HL_BLK[b.t][0]}"></ha-icon><b>${esc(b.title || HL_BLK[b.t][1])}</b>${miss ? `<span class="hle-miss">${miss} Wert fehlt</span>` : ""}
          <span class="hle-tools"><button class="hle-ib${E.sel === i ? " on" : ""}" data-ed="sel" data-i="${i}" aria-label="Baustein bearbeiten">✎</button>
          <button class="hle-ib" data-ed="up" data-i="${i}" ${i === 0 ? "disabled" : ""} aria-label="nach oben">↑</button>
          <button class="hle-ib" data-ed="down" data-i="${i}" ${i === d.length - 1 ? "disabled" : ""} aria-label="nach unten">↓</button>
          <button class="hle-ib" data-ed="rm" data-i="${i}" aria-label="Baustein löschen">✕</button></span></div>
        ${E.sel === i ? `<div class="hle-form">${this._form(i)}</div>` : ""}
        <div class="hle-p">${this._blockHtml(sp[i], true) || `<div class="hld-empty">Noch leer – ✎ antippen.</div>`}</div></div>`;
    }).join("");
    const add = E.add ? `<div class="hle-add">${Object.keys(HL_BLK).map(t => `<button data-ed="add" data-v="${t}"><ha-icon icon="${HL_BLK[t][0]}"></ha-icon><span><b>${HL_BLK[t][1]}</b><small>${HL_BLK_D[t]}</small></span></button>`).join("")}</div>` : "";
    this.innerHTML = `<style>${detailCss}</style><div class="hld hle">
      <div class="hld-box hld-hint">Fenster anpassen: Bausteine mit ↑ ↓ ordnen, mit ✎ einstellen. Gilt für alle HomeLines-Karten.</div>
      ${E.err ? `<div class="hld-box hld-hint err">${esc(E.err)}</div>` : ""}
      ${blocks || `<div class="hld-empty">Das Fenster ist leer.</div>`}
      <div class="hle-bar"><button class="hld-b" data-ed="addopen">+ Baustein</button><button class="hld-b" data-ed="fritz">+ FRITZ!Box-Vorlage</button></div>${add}
      <div class="hle-foot">${this._spec.custom ? `<button class="hld-b" data-ed="reset">Eingebautes Fenster</button>` : ""}<span style="flex:1"></span>
        <button class="hld-b" data-ed="cancel">Abbrechen</button><button class="hle-pri" data-ed="save">Speichern</button></div>
      <div class="hle-pickhost">${E.pick ? this._pickHtml() : ""}</div></div>`;
    const inp = this.querySelector("[data-pq]"); if (inp) inp.focus();
  }
  _values(b) {
    const h = this._hass, names = this._names(b.entities), lv = e => hlLevel(h, b.rules, [e]);
    const t = b.title ? `<div class="hld-t">${esc(b.title)}</div>` : "";
    if (b.style === "list") return `<div class="hld-box">${t}${b.entities.map((e, k) => { const v = this._val(e), miss = !h.states[e];
      const l = miss ? "err" : lv(e) || (v == null ? "mut" : "ok");
      return `<div class="hld-row" data-e="${esc(e)}" style="cursor:pointer"><span class="dot ${l}"></span><span>${esc(miss ? e : names[k])}</span><span class="r">${esc(v ?? (miss ? "Wert fehlt" : "nicht verfügbar"))}</span></div>`; }).join("")}</div>`;
    return `${b.title ? `<div class="hld-t" style="margin:2px 2px 6px">${esc(b.title)}</div>` : ""}<div class="hld-vals">${b.entities.map((e, k) => { const v = this._val(e), miss = !h.states[e];
      return `<div class="hld-v${v == null ? " na" : ""} ${miss ? "miss" : lv(e)}" data-e="${esc(e)}"><div class="hld-n">${esc(miss ? e : names[k])}</div><div class="hld-x">${esc(v ?? (miss ? "Wert fehlt" : "nicht verfügbar"))}</div></div>`; }).join("")}</div>`;
  }
  _blockHtml(b, editing) {
    if (!b) return "";
    if (b.type === "values") return b.entities.length ? this._values(b) : "";
    if (b.type === "chart") return this._chart(b);
    if (b.type === "timeline") return this._timeline(b);
    if (b.type === "phone") return this._phone() || (editing ? `<div class="hld-empty">Notfall-Handy ist nicht eingerichtet.</div>` : "");
    if (b.type === "log") return this._log(b);
    if (b.type === "controls") return b.entities.length ? this._controls(b) : "";
    if (b.type === "hint") return b.text ? `<div class="hld-box hld-hint ${b.tone === "warn" || b.tone === "err" ? b.tone : ""}">${esc(b.text)}</div>` : "";
    return "";
  }
  _paint() {
    const sp = this._spec, h = this._hass;
    if (!sp || !h) return;
    this._bind();
    if (this._edit) { this._paintEdit(); return; }
    if (!this._root) {
      const tools = this._admin() ? `<div class="hld-tools">${sp.custom ? `<span>angepasst</span>` : ""}<button class="hld-b" data-ed="start">✎ Fenster anpassen</button></div>` : "";
      this.innerHTML = `<style>${detailCss}</style><div class="hld">${tools}</div>`;
      this._root = this.querySelector(".hld");
      // Feste Reihenfolge der Bausteine
      this._slots = sp.blocks.map(b => { const d = document.createElement("div"); d.dataset.type = b.type; this._root.appendChild(d); return d; });
      if (!sp.blocks.length) this._root.insertAdjacentHTML("beforeend", `<div class="hld-empty">Dieses Fenster ist leer.</div>`);
    }
    sp.blocks.forEach((b, i) => {
      const slot = this._slots[i];
      if (b.type === "controls") {   // nicht neu zeichnen, während jemand eine Uhrzeit, Zahl oder Auswahl eingibt
        const f = document.activeElement;
        if (f && slot.contains(f) && /^(INPUT|SELECT)$/.test(f.tagName)) return;
      }
      slot.innerHTML = this._blockHtml(b);
    });
  }

}
if (!customElements.get("homelines-detail")) customElements.define("homelines-detail", HomeLinesDetail);

/* Karten einer vorhandenen Dashboard-Seite holen, z. B. "/dashboard-beispiel/internet" */
async function hlViewCards(hass, path) {
  const parts = String(path).replace(/^\/+/, "").split(/[/?#]/);
  let urlPath = parts[0] || null, viewKey = parts[1] || "0";
  if (urlPath === "lovelace") urlPath = null;
  const conf = await hass.callWS({ type: "lovelace/config", url_path: urlPath });
  const views = (conf && conf.views) || [];
  const view = views.find(v => v.path === viewKey) || views[Number(viewKey)] ;
  if (!view) throw new Error("Ansicht fehlt");
  const out = [];
  if (Array.isArray(view.sections)) {
    view.sections.forEach(sec => {
      const span = Number(sec.column_span) || 1, base = 12 * span;
      (sec.cards || []).forEach(c => {
        const go = c.grid_options || {}; let frac = 1;
        if (typeof go.columns === "number") frac = Math.min(1, go.columns / base);
        else if (/tile/.test(c.type || "") && go.columns !== "full") frac = Math.min(1, 6 / base);
        out.push({ cfg: c, frac });
      });
    });
  }
  (view.cards || []).forEach(c => out.push({ cfg: c, frac: 1 }));
  return out;
}
function hlHasInnerPopup(els, hash) {
  return els.some(e => e && e.config && e.config.hash === hash) ||
    els.some(e => e && e._config && e._config.hash === hash);
}

function hlOpenPopup(hass, cardCfg, entryId, opts = {}) {
  if (!document.getElementById("hl-pop-css")) {
    const st = document.createElement("style"); st.id = "hl-pop-css"; st.textContent = popCss; document.head.appendChild(st);
  }
  // Jedes Fenster hat eine eigene Nummer im Browser-Verlauf, damit Fenster übereinander liegen können
  // (z. B. Detailfenster aus der großen Karte im Popup der Mini-Karte) und „Zurück“ nur das oberste schließt.
  const myId = (window.__hlPopSeq = (window.__hlPopSeq || 0) + 1);
  const ov = document.createElement("div");
  ov.className = "hl-pop";
  ov.innerHTML = `<div class="in"><button class="hl-x" aria-label="Schließen">✕</button>${opts.title ? `<p class="pt">${esc(opts.title)}</p>` : ""}</div>`;
  const inner = ov.firstChild, els = [], hashes = new Set();
  let card = null;
  if (opts.showCard !== false) {
    card = document.createElement("homelines-card");
    card.setConfig({ compact: true, ...(cardCfg || {}), ...(entryId ? { entry_id: entryId } : {}) });
    card.hass = hass; inner.appendChild(card); els.push(card);
  }
  if (opts.content) { inner.classList.add("panel"); inner.appendChild(opts.content); opts.content.hass = hass; els.push(opts.content); }
  // Weitere Karten: eine vorhandene Dashboard-Seite (view) oder eine eigene Liste (cards)
  if (opts.view || (opts.cards || []).length) {
    if (opts.view) inner.classList.add("wide");
    const grid = document.createElement("div");
    grid.className = "grid";
    inner.appendChild(grid);
    const msg = t => { grid.innerHTML = `<div class="err" style="color:var(--secondary-text-color)">${esc(t)}</div>`; };
    (async () => {
      let items = (opts.cards || []).map(c => ({ cfg: c, frac: null }));
      if (opts.view) {
        msg("Lade Seite …");
        try { items = await hlViewCards(hass, opts.view); grid.innerHTML = ""; }
        catch (e) { msg(`Seite ${opts.view} nicht gefunden: ${e.message || e}`); return; }
      }
      let helpers = null;
      try { helpers = window.loadCardHelpers ? await window.loadCardHelpers() : null; } catch (e) { helpers = null; }
      const cols = Number(opts.columns) || 2;
      items.forEach(({ cfg, frac }) => {
        if (cfg && cfg.hash) hashes.add(String(cfg.hash));
        let el;
        try {
          if (helpers) el = helpers.createCardElement(cfg);
          else { el = document.createElement(String(cfg.type || "").replace(/^custom:/, "")); el.setConfig(cfg); }
        } catch (e) {
          el = document.createElement("div"); el.className = "err"; el.textContent = `Karte fehlerhaft: ${e.message || e}`;
        }
        let span;
        if (frac != null) span = Math.max(1, Math.min(12, Math.round(frac * 12)));
        else span = (/tile/.test(cfg.type || "") && !cfg.full_width) ? Math.round(12 / cols) : 12;
        el.style.gridColumn = `span ${span}`;
        el.hass = hass; grid.appendChild(el); els.push(el);
      });
    })();
  }
  const show = v => { ov.style.display = v ? "" : "none"; };
  const close = () => {
    ov.remove(); document.removeEventListener("keydown", key); window.removeEventListener("popstate", pop);
    window.removeEventListener("location-changed", loc); window.removeEventListener("hashchange", loc); ov._closed = true;
  };
  const mine = () => history.state && history.state.hlPop === myId;
  const shut = () => { if (mine()) history.back(); else close(); };
  const top = () => { const all = document.querySelectorAll("body > .hl-pop"); return all[all.length - 1] === ov; };
  // Esc gehört dem obersten sichtbaren Fenster – nicht, solange ein HA-Detailfenster darüber liegt
  const key = e => { if (e.key === "Escape" && ov.style.display !== "none" && ov.style.visibility !== "hidden" && top()) shut(); };
  // Zurück-Taste: zurück auf unseren Eintrag = wieder zeigen, Eintrag eines höheren Fensters = nichts tun,
  // weiter zurück = schließen
  const pop = () => {
    if (location.hash) return;
    const st = history.state && history.state.hlPop;
    if (st === myId) { byHash = false; show(true); }
    else if (typeof st === "number" && st > myId) return;
    else close();
  };
  // Öffnet eine Kachel ein Bubble-Popup (#hash), treten wir solange zur Seite
  let byHash = false;
  const loc = () => {
    if (location.hash) {
      if (hashes.has(location.hash) || hlHasInnerPopup(els, location.hash)) return;
      byHash = true; show(false); return;
    }
    if (byHash) {
      byHash = false; show(true);
      if (!mine()) history.replaceState({ ...(history.state || {}), hlPop: myId }, "");
    }
  };
  ov.addEventListener("click", e => { if (e.target === ov || e.target.classList.contains("hl-x")) shut(); });
  document.addEventListener("keydown", key);
  history.pushState({ hlPop: myId }, ""); window.addEventListener("popstate", pop);
  window.addEventListener("location-changed", loc); window.addEventListener("hashchange", loc);
  document.body.appendChild(ov);
  return { card, close, setHass(h) { els.forEach(e => { e.hass = h; }); }, get open() { return !ov._closed; } };
}

class HomeLinesMini extends HTMLElement {
  setConfig(c) {
    this._c = { layout: "bar", throughput_hours: 6, ...(c || {}) };
    if (!["bar", "tile"].includes(this._c.layout)) throw new Error("layout: bar oder tile");
    this._info = null; this._series = null; this._last = null;
    if (this._hass && this.isConnected) this._start();
  }
  static getStubConfig() { return { layout: "tile", name: "Internet" }; }
  getCardSize() { return this._c && this._c.layout === "tile" ? 2 : 1; }
  getGridOptions() { return this._c && this._c.layout === "tile" ? { columns: 6, rows: 2, min_columns: 3 } : { columns: 12, rows: 1, min_columns: 6 }; }

  set hass(h) {
    const first = !this._hass; this._hass = h;
    if (!this.shadowRoot) this._build();
    if (!this._feed && this.isConnected) this._start();
    if (this._pop && this._pop.open) this._pop.setHass(h);
    let changed = false;
    this._ents().forEach(e => { const st = h.states[e]; this._last = this._last || {};
      if (st && st !== this._last[e]) { this._last[e] = st; this._pushPoint(e, st); changed = true; } });
    if (changed) this._paint();
  }
  _ents() {
    // Eigene Sensoren der Karte haben Vorrang, sonst die Geschwindigkeit aus den HomeLines-Optionen
    if (this._c.throughput_entity) return [this._c.throughput_entity, this._c.upload_entity].filter(Boolean);
    const sp = ((this._f && this._f.data && this._f.data.details) || {}).speed || {};
    return [sp.download, sp.upload].filter(Boolean);
  }
  connectedCallback() { if (this._hass && !this._feed) this._start(); }
  disconnectedCallback() {
    if (this._feed) { this._feed.remove(this._onFeed); this._feed = null; }
    if (this._infoSub) { this._infoSub.then(u => u()).catch(() => {}); this._infoSub = null; }
    clearInterval(this._hist); this._hist = null; clearInterval(this._tick); this._tick = null;
  }
  _build() {
    this.attachShadow({ mode: "open" }).innerHTML = `<style>${miniCss}</style><ha-card></ha-card>`;
    this.shadowRoot.querySelector("ha-card").addEventListener("click", () => this._tap());
  }
  _start() {
    if (!this.isConnected) return;
    this._onFeed = this._onFeed || (f => {
      this._f = f;
      const key = this._ents().join("|");
      if (key !== this._entsKey) {
        this._entsKey = key; this._series = null; clearInterval(this._hist);
        if (key) { this._loadHistory(); this._hist = setInterval(() => this._loadHistory(), 300000); }
      }
      this._paint();
    });
    if (this._feed) this._feed.remove(this._onFeed);
    this._feed = hlFeed(this._hass, this._c.entry_id);
    this._feed.add(this._onFeed);
    if (this._infoSub) { this._infoSub.then(u => u()).catch(() => {}); this._infoSub = null; }
    if (this._c.info) this._infoSub = this._hass.connection.subscribeMessage(r => {
      if (r && "result" in r) { this._info = String(r.result); this._paint(); }
    }, { type: "render_template", template: String(this._c.info) });
    clearInterval(this._hist); clearInterval(this._tick);
    this._tick = setInterval(() => this._paint(), 30000);
    this._entsKey = this._ents().join("|");
    if (this._ents().length) { this._loadHistory(); this._hist = setInterval(() => this._loadHistory(), 300000); }
  }
  _tap() {
    const nav = this._c.navigation_path || (this._c.tap_action || {}).navigation_path;
    if (nav) return hlNavigate(nav);
    if (this._c.tap === "none") return;
    this._pop = hlOpenPopup(this._hass, this._c.card, this._c.entry_id,
      { cards: this._c.popup_cards, columns: this._c.popup_columns, view: this._c.popup_view,
        showCard: this._c.popup_show_card ?? (this._c.popup_view ? false : true) });
  }

  /* --- Sparkline aus dem Verlauf */
  async _loadHistory() {
    const ents = this._ents(), hrs = Number(this._c.throughput_hours) || 6;
    try {
      const r = await this._hass.callWS({ type: "history/history_during_period", entity_ids: ents,
        start_time: new Date(Date.now() - hrs * 3600000).toISOString(), minimal_response: true, no_attributes: true,
        significant_changes_only: false });
      this._series = {};
      ents.forEach(e => {
        this._series[e] = ((r && r[e]) || []).map(x => [(x.lu || x.lc || 0) * 1000, parseFloat(x.s)]).filter(p => !isNaN(p[1]) && p[0]);
      });
      this._paint();
    } catch (e) { this._series = this._series || {}; }
  }
  _pushPoint(ent, st) {
    const v = parseFloat(st.state); if (isNaN(v)) return;
    this._series = this._series || {}; (this._series[ent] = this._series[ent] || []).push([Date.now(), v]);
  }
  _buckets(pts) {
    const hrs = Number(this._c.throughput_hours) || 6, t1 = Date.now(), t0 = t1 - hrs * 3600000, N = 48;
    const b = new Array(N).fill(null);
    // Stufenverlauf: jeder Wert gilt bis zum nächsten; je Abschnitt der höchste Wert
    for (let i = 0; i < pts.length; i++) {
      const a = Math.max(pts[i][0], t0), e = i + 1 < pts.length ? pts[i + 1][0] : t1;
      if (e < t0) continue;
      const i0 = Math.max(0, Math.floor((a - t0) / (t1 - t0) * N)), i1 = Math.min(N - 1, Math.floor((e - t0) / (t1 - t0) * N));
      for (let k = i0; k <= i1; k++) b[k] = Math.max(b[k] ?? 0, pts[i][1]);
    }
    return b;
  }
  _sparkSvg() {
    // Jede Linie bekommt ihren eigenen Bereich und Maßstab (min…max), damit auch kleine
    // Unterschiede sichtbar werden. Sehr kleine Schwankungen werden nicht künstlich aufgeblasen.
    const S = this._series || {}, N = 48;
    const bs = this._ents().map(e => this._buckets(S[e] || []));
    const bands = bs.length > 1 ? [[2, 15], [18, 29]] : [[2, 29]];
    const fmt = xy => xy.map(p => p.map(n => n.toFixed(1)).join(",")).join(" ");
    const paths = bs.map((b, k) => {
      const vals = b.filter(v => v != null); if (vals.length < 2) return null;
      let lo = Math.min(...vals), hi = Math.max(...vals);
      const minSpan = Math.max(hi * 0.15, 1);
      if (hi - lo < minSpan) { const mid = (hi + lo) / 2; lo = mid - minSpan / 2; hi = mid + minSpan / 2; }
      if (lo < 0 || lo < (hi - lo) * 0.3) lo = Math.max(0, Math.min(lo, 0));
      const [top, bot] = bands[k];
      return b.map((v, i) => v == null ? null : [i / (N - 1) * 100, bot - (v - lo) / (hi - lo) * (bot - top)]).filter(Boolean);
    });
    if (!paths[0]) return "";
    const d = paths[0], bot0 = bands[0][1] + 1;
    const area = `${d[0][0].toFixed(1)},${bot0} ${fmt(d)} ${d[d.length - 1][0].toFixed(1)},${bot0}`;
    const up = paths[1] ? `<polyline points="${fmt(paths[1])}" fill="none" stroke="var(--hl-up,var(--primary-color,#03a9f4))" stroke-width="1.5" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>` : "";
    return `<svg class="sp" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true">
      <polygon points="${area}" fill="var(--c)" opacity=".15"/><polyline points="${fmt(d)}" fill="none" stroke="var(--c)" stroke-width="1.6" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>${up}</svg>`;
  }

  /* --- Inhalt je Betriebsart */
  _model() {
    const f = this._f, s = f && f.data;
    const name = this._c.name || "Internet";
    if (!s) return { cls: "", c: "var(--secondary-text-color)", icon: "mdi:web-sync", n: name, t: f && f.state === "missing" ? "HomeLines antwortet nicht" : tr.connecting };
    const mode = s.mode, mon = s.monitor || {}, c = s.counts || {}, u = s.usage || {};
    const active = (s.wans || []).find(w => w.active), lc = (this._c.card || {}).lines || {};
    const wname = w => w ? ((lc[w.id] || {}).name || w.name) : "";
    const [e1, e2] = this._ents();
    const num = e => { const st = e && this._hass.states[e]; return st && !isNaN(parseFloat(st.state)) ? st : null; };
    const tp = num(e1), up = num(e2);
    const tpTxt = tp ? `↓ ${Math.round(parseFloat(tp.state)).toLocaleString("de-DE")}${up ? ` · ↑ ${Math.round(parseFloat(up.state)).toLocaleString("de-DE")}` : ""} ${tp.attributes.unit_of_measurement || ""}`.trim() : "";
    const lat = mon.latency != null ? `${Math.round(mon.latency)} ms` : "";
    const stale = f.state !== "ok" ? " · Stand " + hm(new Date(f.at)) : "";
    if (s.assistant && s.assistant.kind === "return" && mode === "normal")
      return { cls: "warn", c: "var(--hl-warn)", icon: "mdi:cellphone-arrow-down", n: `${name} · ${wname(active) || "Hauptleitung"}`, t: "Hauptleitung zurück – Notfall-Handy zurückstellen" + stale };
    if (mode === "normal" && s.pending_since)
      return { cls: "warn", c: "var(--hl-warn)", icon: "mdi:web-clock", n: name, t: "Hauptleitung antwortet nicht – wird geprüft" + stale };
    if (mode === "normal" && mon.internet === false)
      return { cls: "err", c: "var(--hl-err)", icon: "mdi:web-off", n: `${name} · Kein Internet`, t: `seit ${when((mon.current_outage || {}).start)}` + stale };
    if (mode === "emergency") {
      const t = `${c.online_now ?? "?"} von ${c.total ?? "?"} online · ${mb(u.mb)} · ${eur(u.cost)}`;
      return { cls: "warn", c: "var(--hl-warn)", icon: "mdi:signal-cellular-3", n: this._c.layout === "tile" ? "Notbetrieb" : `Notbetrieb · ${wname(active) || s.backup_wan || ""}`, t: t + stale, pill: "Tagesflat?" };
    }
    if (mode === "dayflat") {
      const left = s.restore_at ? Math.max(0, new Date(s.restore_at) - Date.now()) : 0;
      const h = Math.floor(left / 3600000), m = Math.floor(left % 3600000 / 60000);
      return { cls: "", c: "var(--hl-warn)", icon: "mdi:timer-sand", n: this._c.layout === "tile" ? `Tagesflat ${h}:${p2(m)} h` : `Tagesflat · noch ${h}:${p2(m)} h`, t: `${c.online_now ?? "?"} von ${c.total ?? "?"} online · ${mb(u.mb)} · zurück ${when(s.restore_at)}` + stale };
    }
    const parts = [wname(active), tpTxt, lat].filter(Boolean);
    return { cls: "", c: "var(--hl-ok)", icon: "mdi:web-check", n: name, t: (this._info != null && this._info !== "" ? this._info : parts.join(" · ")) + stale };
  }
  _dots() {
    const s = this._f && this._f.data; if (!s) return "";
    const lc = (this._c.card || {}).lines || {};
    return `<div class="dots">${(s.wans || []).filter(w => !(lc[w.id] || {}).hide).map(w => {
      const act = w.active || (w.backup && s.mode !== "normal" && w.state === "online");
      const cold = w.backup && s.mode === "normal" && w.state !== "online";
      const na = w.state === "unknown" && !w.entity_id;
      const k = act ? "a" : na ? "na" : cold ? "" : w.state === "offline" ? "x" : w.state === "online" ? "o" : "";
      return `<span class="d ${k}" title="${esc((lc[w.id] || {}).name || w.name)}: ${esc(tr.lineStates[w.state] || w.state)}"></span>`;
    }).join("")}</div>`;
  }
  _paint() {
    if (!this.shadowRoot || !this._c) return;
    const m = this._model(), card = this.shadowRoot.querySelector("ha-card");
    card.className = m.cls; card.style.setProperty("--c", m.c);
    const pill = m.pill ? `<span class="pill">${esc(m.pill)}</span>` : "";
    const sp = this._ents().length && (!this._f || !this._f.data || this._f.data.mode === "normal") ? this._sparkSvg() : "";
    if (this._c.layout === "tile") {
      card.innerHTML = `<div class="t"><div class="top"><div class="ic"><ha-icon icon="${m.icon}"></ha-icon></div>${this._dots()}</div>
        <div class="n"><span style="overflow:hidden;text-overflow:ellipsis">${esc(m.n)}</span>${pill}</div><div class="s">${esc(m.t)}</div>${sp}</div>`;
    } else {
      card.innerHTML = `<div class="w"><div class="ic"><ha-icon icon="${m.icon}"></ha-icon></div>
        <div class="tx"><div class="n"><span style="overflow:hidden;text-overflow:ellipsis">${esc(m.n)}</span>${pill}</div><div class="s">${esc(m.t)}</div></div>
        ${sp}${this._dots()}<ha-icon class="ch" icon="mdi:chevron-right"></ha-icon></div>`;
    }
  }
}

/* ------------------------------------------------------------------ Grafische Editoren
   Alle drei Karten bekommen einen Editor mit ha-form. Er schreibt dieselben Schlüssel wie YAML;
   Schlüssel, die der Editor nicht kennt (z. B. popup_cards), bleiben unverändert erhalten.        */
const ED_LABEL = {
  layout: "Darstellung", name: "Name", title: "Titel", compact: "Kompakt (im Normalbetrieb nur Kopf, Leitungen und Kennzahlen)",
  show_devices: "Geräte-Knopf zeigen", overview: "Übersicht zeigen (Notfall-Strecke, Leitungen, Geschwindigkeit, Ausfälle)", throughput_entity: "Sensor Download (Verlauf)", upload_entity: "Sensor Upload (zweite Linie)",
  throughput_hours: "Verlauf über Stunden", info: "Eigene zweite Zeile (Vorlage)", navigation_path: "Beim Antippen öffnen (Pfad oder #popup)",
  popup_view: "Dashboard-Seite als Popup (Pfad)", popup_columns: "Spalten im Popup", popup_show_card: "HomeLines-Karte im Popup zeigen",
  icon: "Symbol", text: "Text (Vorlage)", warning: "Gelb, wenn (Vorlage)", error: "Rot, wenn (Vorlage)", entity: "Entität (Details beim Antippen)",
  tap: "Beim Antippen öffnen (Pfad oder #popup)", entities: "Entitäten", combine: "Anzeige",
  warn_unavailable: "Gelb, wenn eine Entität nicht erreichbar ist", warn_below: "Gelb unter", warn_above: "Gelb über",
  error_below: "Rot unter", error_above: "Rot über", hours: "Verlauf im Fenster (Stunden)", hide: "In der Mini-Karte ausblenden", na_text: "Text, wenn nicht angeschlossen",
};
const ED_HELP = {
  name: "", info: "Leer: aktive Leitung, Download und Latenz. Beispiel: {{ state_attr('sensor.homelines_active_wan', 'name') }}",
  navigation_path: "Leer: die große HomeLines-Karte öffnet sich als Popup.",
  popup_view: "Teil der Adresse ab dem ersten „/“, z. B. /dashboard-beispiel/internet. Weitere Karten fürs Popup (popup_cards) im Code-Editor.",
  warning: "Ergebnis true/on/ja färbt die Kachel gelb.", error: "Ergebnis true/on/ja färbt die Kachel rot.",
  entities: "Die Werte dieser Entitäten zeigt die Kachel an. Ein Tipp öffnet ein Fenster mit allen Werten und ihrem Verlauf.",
  text: "Nur wenn die Auswahl oben nicht reicht. Hat Vorrang vor „Anzeige“.",
  tap: "Leer: eingebautes Detailfenster der Leitung (Werte unter HomeLines → Konfigurieren → Detailansichten).",
  throughput_entity: "Leer: Geschwindigkeit aus HomeLines → Konfigurieren → Detailansichten.",
};
const ED_LINE_HELP = "Nur für diese Karte. Den Namen für alle Karten stellst du in HomeLines → Konfigurieren → Leitungen ein.";

function hlClean(v) {
  if (Array.isArray(v)) return v;
  if (v && typeof v === "object") {
    const out = {};
    Object.entries(v).forEach(([k, x]) => { const c = hlClean(x); if (c !== undefined) out[k] = c; });
    return Object.keys(out).length ? out : undefined;
  }
  return v === "" || v === null || v === undefined ? undefined : v;
}
function hlSchemaKeys(schema) {
  const keys = [];
  (schema || []).forEach(s => { if (s.type === "expandable" && s.flatten) keys.push(...hlSchemaKeys(s.schema)); else if (s.name) keys.push(s.name); });
  return keys;
}

class HomeLinesEditorBase extends HTMLElement {
  setConfig(c) { this._config = { ...(c || {}) }; this._render(); }
  set hass(h) { this._hass = h; this._render(); }
  _schema() { return []; }
  _render() {
    if (!this._hass || !this._config) return;
    if (!this._form) {
      this._form = document.createElement("ha-form");
      this._form.computeLabel = s => s.title || ED_LABEL[s.name] || s.name;
      this._form.computeHelper = s => s.helper || ED_HELP[s.name] || "";
      this._form.addEventListener("value-changed", e => { e.stopPropagation(); this._changed(e.detail.value); });
      this.appendChild(this._form);
    }
    this._form.hass = this._hass;
    this._form.schema = this._schema();
    this._form.data = this._formData();
  }
  _formData() { return this._config; }
  _changed(v) {
    const out = { ...this._config };
    hlSchemaKeys(this._schema()).forEach(k => { if (v && k in v) out[k] = v[k]; else delete out[k]; });
    Object.entries(this._defaults || {}).forEach(([k, d]) => { if (out[k] === d) delete out[k]; });
    const cfg = { type: this._config.type, ...(hlClean({ ...out, type: undefined }) || {}) };
    if (!cfg.type) delete cfg.type;
    this._config = cfg;
    this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: cfg }, bubbles: true, composed: true }));
  }
}

class HomeLinesMiniEditor extends HomeLinesEditorBase {
  _schema() {
    return [
      { name: "layout", selector: { select: { mode: "dropdown", options: [
        { value: "tile", label: "Kachel" }, { value: "bar", label: "Leiste (volle Breite)" }] } } },
      { name: "name", selector: { text: {} } },
      { type: "expandable", flatten: true, title: "Verlauf", icon: "mdi:chart-line", schema: [
        { name: "throughput_entity", selector: { entity: { domain: "sensor" } } },
        { name: "upload_entity", selector: { entity: { domain: "sensor" } } },
        { name: "throughput_hours", selector: { number: { min: 1, max: 168, step: 1, mode: "box", unit_of_measurement: "h" } } },
      ] },
      { name: "info", selector: { template: {} } },
      { type: "expandable", flatten: true, title: "Beim Antippen", icon: "mdi:gesture-tap", schema: [
        { name: "navigation_path", selector: { text: {} } },
        { name: "popup_view", selector: { text: {} } },
        { name: "popup_columns", selector: { number: { min: 1, max: 4, step: 1, mode: "box" } } },
        { name: "popup_show_card", selector: { boolean: {} } },
      ] },
    ];
  }
  _render() {
    if (this._config && this._config.layout === undefined) this._config = { ...this._config, layout: "bar" };
    super._render();
  }
}

function hlLineIds(hass, config) {
  const st = hass && hass.states && hass.states["sensor.homelines_active_wan"];
  const ids = ((st && st.attributes && st.attributes.lines) || []).map(l => l.id);
  const names = Object.fromEntries(((st && st.attributes && st.attributes.lines) || []).map(l => [l.id, l.name]));
  Object.keys((config && config.lines) || {}).forEach(id => { if (!ids.includes(id)) ids.push(id); });
  if (!ids.length) ids.push("WAN1", "WAN2", "WAN3");
  return ids.map(id => ({ id, name: names[id] }));
}

const HL_TILE_SLOTS = ["t1", "t2", "t3", "t4"];
class HomeLinesCardEditor extends HomeLinesEditorBase {
  constructor() { super(); this._defaults = { overview: true }; }
  _formData() {
    const base = { overview: true, ...this._config };
    // ha-form erwartet für verschachtelte Abschnitte ein Objekt, auch wenn noch nichts eingestellt ist
    const lines = { ...(this._config.lines || {}) };
    hlLineIds(this._hass, this._config).forEach(l => { lines[l.id] = { ...(lines[l.id] || {}) }; });
    const tiles_ed = {};
    HL_TILE_SLOTS.forEach((k, i) => { tiles_ed[k] = { ...((this._config.tiles || [])[i] || {}) }; });
    return { ...base, lines, overview_hide: { ...(this._config.overview_hide || {}) }, tiles_ed };
  }
  _changed(v) {
    // Plätze 1–4 im Formular ↔ Liste „tiles:“ in der Karte
    const v2 = { ...(v || {}) }, ed = v2.tiles_ed || {}; delete v2.tiles_ed;
    if (v2.overview_hide) v2.overview_hide = Object.fromEntries(Object.entries(v2.overview_hide).filter(([, x]) => x === true));
    const keep = (this._config.tiles || []).slice(HL_TILE_SLOTS.length);
    const tiles = [...HL_TILE_SLOTS.map(k => hlClean({ ...(ed[k] || {}) })).filter(Boolean), ...keep];
    this._config = { ...this._config, tiles: tiles.length ? tiles : undefined };
    super._changed(v2);
  }
  _schema() {
    return [
      { name: "title", selector: { text: {} } },
      { name: "compact", selector: { boolean: {} } },
      { name: "overview", selector: { boolean: {} } },
      { type: "expandable", name: "overview_hide", title: "Übersicht: Zeilen ausblenden", icon: "mdi:eye-off-outline",
        schema: [{ name: "backup", title: "Notfall-Strecke", selector: { boolean: {} } },
          ...hlLineIds(this._hass, this._config).map(l => ({ name: l.id, title: l.name && l.name !== l.id ? `${l.name} (${l.id})` : l.id, selector: { boolean: {} } })),
          { name: "speed", title: "Geschwindigkeit", selector: { boolean: {} } },
          { name: "outages", title: "Ausfälle und Verlauf", selector: { boolean: {} } }] },
      { type: "expandable", name: "tiles_ed", title: "Eigene Kacheln in der Karte", icon: "mdi:view-grid-plus-outline",
        schema: HL_TILE_SLOTS.map((k, i) => {
          const t = (this._config.tiles || [])[i];
          return { type: "expandable", name: k, title: t && t.name ? `Kachel ${i + 1} · ${t.name}` : `Kachel ${i + 1}`, schema: hlTileSchema() };
        }) },
      { type: "expandable", name: "lines", title: "Leitungen in dieser Karte", icon: "mdi:wan",
        schema: hlLineIds(this._hass, this._config).map(l => ({
          type: "expandable", name: l.id, title: l.name && l.name !== l.id ? `${l.id} · ${l.name}` : l.id, schema: [
            { name: "name", selector: { text: {} }, helper: ED_LINE_HELP },
            { name: "tap", selector: { text: {} } },
            { name: "info", selector: { template: {} }, helper: "Zusätzliche Zeile in der Leitungskachel." },
            { name: "hide", selector: { boolean: {} } },
          ] })) },
    ];
  }
}

class HomeLinesTileEditor extends HomeLinesEditorBase {
  _schema() { return hlTileSchema(); }
}
function hlTileSchema() {
    return [
      { name: "name", required: true, selector: { text: {} } },
      { name: "icon", selector: { icon: {} } },
      { name: "entities", selector: { entity: { multiple: true } } },
      { name: "combine", selector: { select: { mode: "dropdown", options: [
        { value: "sum", label: "Summe" }, { value: "single", label: "Einzelwert (erste Entität)" },
        { value: "list", label: "Alle Werte nebeneinander" }, { value: "avg", label: "Durchschnitt" },
        { value: "min", label: "Kleinster Wert" }, { value: "max", label: "Größter Wert" }] } } },
      { type: "expandable", flatten: true, title: "Warnfarben", icon: "mdi:alert-outline", schema: [
        { name: "warn_unavailable", selector: { boolean: {} } },
        { name: "warn_below", selector: { number: { mode: "box", step: "any" } } },
        { name: "warn_above", selector: { number: { mode: "box", step: "any" } } },
        { name: "error_below", selector: { number: { mode: "box", step: "any" } } },
        { name: "error_above", selector: { number: { mode: "box", step: "any" } } },
      ] },
      { type: "expandable", flatten: true, title: "Beim Antippen", icon: "mdi:gesture-tap", schema: [
        { name: "hours", selector: { number: { min: 1, max: 720, step: 1, mode: "box", unit_of_measurement: "h" } } },
        { name: "navigation_path", selector: { text: {} }, helper: "Leer: Fenster mit den Werten und dem Verlauf der Entitäten." },
      ] },
      { type: "expandable", flatten: true, title: "Erweitert: Vorlagen", icon: "mdi:code-braces", schema: [
        { name: "text", selector: { template: {} } },
        { name: "warning", selector: { template: {} } },
        { name: "error", selector: { template: {} } },
      ] },
    ];
}

[["homelines-card-editor", HomeLinesCardEditor], ["homelines-mini-editor", HomeLinesMiniEditor],
 ["homelines-tile-editor", HomeLinesTileEditor]].forEach(([n, c]) => { if (!customElements.get(n)) customElements.define(n, c); });
HomeLinesCard.getConfigElement = () => document.createElement("homelines-card-editor");
HomeLinesMini.getConfigElement = () => document.createElement("homelines-mini-editor");
HomeLinesTile.getConfigElement = () => document.createElement("homelines-tile-editor");

if (!customElements.get("homelines-mini")) {
  customElements.define("homelines-mini", HomeLinesMini);
  window.customCards = window.customCards || [];
  window.customCards.push({ type: "homelines-mini", name: "HomeLines Mini", description: "Kleine Statusleiste oder Kachel, Klick öffnet die große Karte", preview: false });
}

if (!customElements.get("homelines-tile")) {
  customElements.define("homelines-tile", HomeLinesTile);
  window.customCards = window.customCards || [];
  window.customCards.push({ type: "homelines-tile", name: "HomeLines Kachel", description: "Kachel mit Vorlagen-Text und Warnfarben", preview: false });
}

if (!customElements.get("homelines-card")) {
  customElements.define("homelines-card", HomeLinesCard);
  window.customCards = window.customCards || [];
  window.customCards.push({ type: "homelines-card", name: "HomeLines", description: "Internet Monitor & Mobile Failover", preview: false });
  console.info(`%c HOMELINES %c ${HL_VERSION} `, "background:#03a9f4;color:#fff", "");
}
