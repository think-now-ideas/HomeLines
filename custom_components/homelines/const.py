"""Konstanten für HomeLines."""

from __future__ import annotations

DOMAIN = "homelines"
NAME = "HomeLines"
VERSION = "0.8.1"

PLATFORMS = ["binary_sensor", "button", "sensor", "switch", "time"]

# --- Router-Anbindung -------------------------------------------------------
CONF_ROUTER_TYPE = "router_type"
ROUTER_UNIFI = "unifi"
ROUTER_SWITCHES = "switches"
ROUTER_SCRIPTS = "scripts"
ROUTER_NONE = "none"
ROUTER_TYPES = [ROUTER_UNIFI, ROUTER_SWITCHES, ROUTER_SCRIPTS, ROUTER_NONE]

CONF_HOST = "host"
CONF_API_KEY = "api_key"
CONF_SITE = "site"
CONF_VERIFY_SSL = "verify_ssl"
CONF_PRIMARY_WAN_NET = "primary_wan_network"  # UniFi: Netzwerk-ID der Hauptleitung
CONF_PRIMARY_WAN_LABEL = "primary_wan_label"  # {"name", "group"} dazu, falls UniFi die ID neu vergibt

CONF_SWITCH_ENTITIES = "switch_entities"  # Schalter je Gerät (an = Internet erlaubt)
CONF_SCRIPT_BLOCK = "script_block"
CONF_SCRIPT_UNBLOCK = "script_unblock"
CONF_TRACKER_ENTITIES = "tracker_entities"  # Geräteliste für die Skript-Anbindung

# --- Leitungen --------------------------------------------------------------
CONF_ACTIVE_WAN_ENTITY = "active_wan_entity"
CONF_BACKUP_WAN = "backup_wan"
CONF_WAN_STATUS_ENTITIES = "wan_status_entities"
CONF_SPEEDTEST_SWITCH = "speedtest_switch"
# Eigene Anzeigenamen der Leitungen, gelten für alle Karten (Schlüssel line_name_wan1 … wan4)
LINE_NAME_KEYS = {f"line_name_wan{i}": f"WAN{i}" for i in range(1, 5)}
# Detailansichten (ab 0.8.0): Sensoren je Leitung, Geschwindigkeit, Notfall-Strecke
LINE_DETAIL_KEYS = {f"details_wan{i}": f"WAN{i}" for i in range(1, 5)}
LINE_HISTORY_KEYS = {f"history_wan{i}": f"WAN{i}" for i in range(1, 5)}
CONF_SPEED_DOWN = "speed_download"
CONF_SPEED_UP = "speed_upload"
CONF_BACKUP_EXTRA = "backup_extra"
CONF_SPEED_EXTRA = "speed_extra"

# Erkennung der Hauptleitung (routerneutral)
CONF_DETECTION = "detection"
DETECT_ACTIVE_WAN = "active_wan"  # Sensor nennt die aktive Leitung
DETECT_PRIMARY_OFF = "primary_off"  # Binärsensor der Hauptleitung ist aus
DETECT_CUSTOM = "custom"  # eigener Binärsensor: an = Hauptleitung weg
DETECT_MONITOR = "monitor"  # eigene Pings von HomeLines
DETECTIONS = [DETECT_ACTIVE_WAN, DETECT_PRIMARY_OFF, DETECT_CUSTOM, DETECT_MONITOR]
CONF_PRIMARY_STATUS_ENTITY = "primary_status_entity"
CONF_CUSTOM_DOWN_ENTITY = "custom_down_entity"
CONF_DETECT_DELAY = "detect_delay"  # Sekunden, bevor ein Ausfall als echt gilt
DEFAULT_DELAY_WARM = 0
DEFAULT_DELAY_COLD = 180

# Bereitschaft der Backup-Leitung
CONF_STANDBY = "standby"
STANDBY_WARM = "warm"  # Backup ständig verbunden, Router schaltet selbst um
STANDBY_COLD = "cold"  # Backup aus, wird im Ausfall von Hand eingeschaltet
STANDBYS = [STANDBY_WARM, STANDBY_COLD]

# --- Monitor ----------------------------------------------------------------
CONF_TARGETS = "targets"
CONF_ROUTER_IP = "router_ip"
CONF_INTERVAL = "interval"
CONF_EMERGENCY_INTERVAL = "emergency_interval"
CONF_PING_COUNT = "ping_count"
CONF_FAILURES = "failures_before_offline"
DEFAULT_TARGETS = "1.1.1.1, 8.8.8.8"
DEFAULT_INTERVAL = 30
DEFAULT_EMERGENCY_INTERVAL = 120
DEFAULT_PING_COUNT = 3
DEFAULT_FAILURES = 2

# --- Tarif ------------------------------------------------------------------
CONF_PROVIDER = "provider"
CONF_PRICE_PER_MB = "price_per_mb"  # Cent
CONF_DAYFLAT_PRICE = "dayflat_price"  # Euro
CONF_DAYFLAT_HOURS = "dayflat_hours"
CONF_BUFFER_MIN = "buffer_minutes"
CONF_START_BALANCE = "start_balance"  # Euro
CONF_INCLUDED_MB = "included_mb"
CONF_BOOKING_URL = "booking_url"
DEFAULT_PROVIDER = ""
DEFAULT_PRICE_PER_MB = 3.0
DEFAULT_DAYFLAT_PRICE = 7.99
DEFAULT_DAYFLAT_HOURS = 24
DEFAULT_BUFFER_MIN = 30
DEFAULT_START_BALANCE = 0.0
DEFAULT_INCLUDED_MB = 0

# --- Handy ------------------------------------------------------------------
CONF_PHONE_RX = "phone_rx"
CONF_PHONE_TX = "phone_tx"
CONF_PHONE_BATTERY = "phone_battery"
CONF_PHONE_CHARGER = "phone_charger"
CONF_PHONE_MOBILE_DATA = "phone_mobile_data"
CONF_PHONE_NETWORK = "phone_network"
CONF_PHONE_SIGNAL = "phone_signal"
CONF_PHONE_OPERATOR = "phone_operator"
CONF_PHONE_WIFI = "phone_wifi"
CONF_PHONE_STALE_MIN = "phone_stale_minutes"
DEFAULT_PHONE_STALE_MIN = 30
CONF_PHONE_NOTIFY = "phone_notify"  # notify-Dienst der App am Handy (Weckruf)
CONF_PHONE_WAKE_MIN = "phone_wake_minutes"
DEFAULT_PHONE_WAKE_MIN = 10
WAKE_MESSAGE = "command_update_sensors"
PHONE_KEYS = [
    CONF_PHONE_RX, CONF_PHONE_TX, CONF_PHONE_BATTERY, CONF_PHONE_CHARGER,
    CONF_PHONE_MOBILE_DATA, CONF_PHONE_NETWORK, CONF_PHONE_SIGNAL, CONF_PHONE_OPERATOR, CONF_PHONE_WIFI,
]

# --- Benachrichtigungen -----------------------------------------------------
CONF_NOTIFY = "notify_services"  # alt (0.1.0): Liste von Diensten, wird migriert
CONF_NOTIFY_TARGETS = "notify_targets"  # [{id, label, service, recipient, sms}]
CONF_NOTIFY_ROUTES = "notify_routes"  # {meldung: [target-id, ...]}
CONF_BACKUP_DOWN_MIN = "backup_down_minutes"
DEFAULT_BACKUP_DOWN_MIN = 10
MSG_EMERGENCY = "emergency"
MSG_FLAT_WARNING = "flat_warning"
MSG_FLAT_EXPIRED = "flat_expired"
MSG_RESTORED = "restored"
MSG_RECONNECT_FAILED = "reconnect_failed"
MSG_BACKUP_DOWN = "backup_down"
MSG_PHONE_SILENT = "phone_silent"
MESSAGES = [MSG_EMERGENCY, MSG_FLAT_WARNING, MSG_FLAT_EXPIRED, MSG_RESTORED,
            MSG_BACKUP_DOWN, MSG_PHONE_SILENT, MSG_RECONNECT_FAILED]

# --- Gruppen ----------------------------------------------------------------
CONF_DEFAULT_GROUP = "default_group"
GROUP_ALWAYS = "always"
GROUP_DAYFLAT = "dayflat"
GROUP_NEVER = "never"
GROUPS = [GROUP_ALWAYS, GROUP_DAYFLAT, GROUP_NEVER]
DEFAULT_GROUP = GROUP_DAYFLAT

# --- Neueinwahl -------------------------------------------------
CONF_RECONNECT_ENABLED = "reconnect_enabled"
CONF_SSH_HOST = "ssh_host"
CONF_SSH_PORT = "ssh_port"
CONF_SSH_USER = "ssh_user"
CONF_SSH_PASSWORD = "ssh_password"
CONF_PPP_INTERFACE = "ppp_interface"
CONF_RECONNECT_METHOD = "reconnect_method"
CONF_RECONNECT_TIME = "reconnect_time"
METHOD_PPPD_HUP = "pppd_hup"
METHOD_IP_LINK = "ip_link"
METHOD_HA_ACTION = "ha_action"  # Button, Skript oder Schalter in HA (z. B. FRITZ!Box „Neu verbinden“)
METHODS = [METHOD_PPPD_HUP, METHOD_IP_LINK, METHOD_HA_ACTION]
SSH_METHODS = [METHOD_PPPD_HUP, METHOD_IP_LINK]
CONF_RECONNECT_ENTITY = "reconnect_entity"
CONF_WAN_IP_ENTITY = "wan_ip_entity"
DEFAULT_SSH_PORT = 22
DEFAULT_SSH_USER = "root"
DEFAULT_PPP_INTERFACE = "ppp1"
DEFAULT_RECONNECT_TIME = "04:00:00"
RECONNECT_WAIT = 90
RECONNECT_POLL = 3
RECONNECT_GRACE = 180  # Sekunden, in denen ein Failover als geplant gilt

# --- Zustände ---------------------------------------------------------------
MODE_NORMAL = "normal"
MODE_EMERGENCY = "emergency"
MODE_DAYFLAT = "dayflat"

RESULT_NEW_IP = "ok_new_ip"
RESULT_SAME_IP = "ok_same_ip"
RESULT_NO_EFFECT = "no_effect"
RESULT_ERROR = "error"
RESULT_TRIGGERED = "triggered"  # ausgelöst, Wirkung nicht prüfbar

# --- Ereignisse -------------------------------------------------------------
EVENT_OUTAGE_STARTED = f"{DOMAIN}_outage_started"
EVENT_OUTAGE_ENDED = f"{DOMAIN}_outage_ended"
EVENT_MODE_CHANGED = f"{DOMAIN}_mode_changed"
EVENT_RECONNECTED = f"{DOMAIN}_reconnected"
EVENT_BLOCK = f"{DOMAIN}_block"  # für die Skript-Anbindung und eigene Automationen

SIGNAL_UPDATE = f"{DOMAIN}_update_{{}}"

STORAGE_VERSION = 1
HISTORY_DAYS = 365
RECENT_OUTAGES = 20
CLIENT_MAX_AGE_DAYS = 30

CARD_URL = "/homelines_static/homelines-card.js"

# --- Umstieg von LineGuard (Vorgänger unter anderem Namen) -------------------
LEGACY_DOMAIN = "lineguard"
LEGACY_ROUTE_DESCRIPTION = "LineGuard Notbetrieb"
CONF_IMPORTED_FROM = "imported_from"  # Eintrags-ID der übernommenen LineGuard-Einrichtung

# --- Reparatur-Hinweise ----------------------------------------------------
ISSUE_LEGACY = "legacy_running"
ISSUE_WAN = "primary_wan_missing"
