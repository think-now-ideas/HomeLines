"""Sensoren von HomeLines."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfDataRate, UnitOfInformation, UnitOfTime
from homeassistant.helpers.entity import EntityCategory
from homeassistant.util import dt as dt_util

from .const import DOMAIN, MODE_DAYFLAT, MODE_EMERGENCY, MODE_NORMAL
from .entity import HomeLinesEntity
from .hub import HomeLinesHub


def _ts(val):
    return dt_util.parse_datetime(val) if val else None


@dataclass(frozen=True, kw_only=True)
class HLSensor(SensorEntityDescription):
    value: Callable[[HomeLinesHub], Any]
    attrs: Callable[[HomeLinesHub], dict] | None = None


SENSORS: list[HLSensor] = [
    # Notbetrieb
    HLSensor(key="status", device_class=SensorDeviceClass.ENUM,
             options=[MODE_NORMAL, MODE_EMERGENCY, MODE_DAYFLAT], icon="mdi:shield-sync",
             value=lambda h: h.mode,
             attrs=lambda h: {"since": h.data["mode"].get("since"), "active_wan": h.active_wan(),
                              "backup_wan": h.backup_wan(), "planned": h._planned(),
                              "router_error": h.router_error}),
    HLSensor(key="active_wan", icon="mdi:wan", value=lambda h: h.active_wan(),
             attrs=lambda h: {"lines": h.wan_lines()}),
    HLSensor(key="restore_at", device_class=SensorDeviceClass.TIMESTAMP, icon="mdi:timer-sand",
             value=lambda h: _ts(h.data["mode"].get("restore_at"))),
    HLSensor(key="dayflat_end", device_class=SensorDeviceClass.TIMESTAMP, icon="mdi:calendar-clock",
             value=lambda h: _ts(h.data["mode"].get("flat_end")),
             attrs=lambda h: {"booked_at": h.data["mode"].get("booked_at")}),
    HLSensor(key="devices_online", icon="mdi:devices", native_unit_of_measurement="Geräte",
             value=lambda h: h.counts()["online_now"], attrs=lambda h: h.counts()),
    # Kosten
    HLSensor(key="usage", device_class=SensorDeviceClass.DATA_SIZE,
             native_unit_of_measurement=UnitOfInformation.MEGABYTES, suggested_display_precision=1,
             state_class=SensorStateClass.TOTAL, icon="mdi:swap-vertical",
             value=lambda h: round(h.data["usage"]["mb"], 1),
             attrs=lambda h: {"reset_at": h.data["usage"]["reset_at"], "breakeven_mb": h.breakeven_mb()}),
    HLSensor(key="cost", device_class=SensorDeviceClass.MONETARY, native_unit_of_measurement="EUR",
             state_class=SensorStateClass.TOTAL, suggested_display_precision=2,
             value=lambda h: round(h.data["usage"]["cost"], 2),
             attrs=lambda h: {"dayflats": h.data["usage"].get("flats", 0)}),
    HLSensor(key="balance", device_class=SensorDeviceClass.MONETARY, native_unit_of_measurement="EUR",
             suggested_display_precision=2, value=lambda h: h.balance()),
    # Monitor
    HLSensor(key="latency", native_unit_of_measurement=UnitOfTime.MILLISECONDS,
             state_class=SensorStateClass.MEASUREMENT, icon="mdi:timer-outline",
             value=lambda h: h.latency),
    HLSensor(key="packet_loss", native_unit_of_measurement=PERCENTAGE,
             state_class=SensorStateClass.MEASUREMENT, icon="mdi:package-variant-remove",
             value=lambda h: h.loss),
    HLSensor(key="outages_24h", icon="mdi:counter", state_class=SensorStateClass.MEASUREMENT,
             value=lambda h: h.outage_stats()["outages_24h"]),
    HLSensor(key="outages_7d", icon="mdi:counter", state_class=SensorStateClass.MEASUREMENT,
             value=lambda h: h.outage_stats()["outages_7d"]),
    HLSensor(key="outages_30d", icon="mdi:counter", state_class=SensorStateClass.MEASUREMENT,
             value=lambda h: h.outage_stats()["outages_30d"]),
    HLSensor(key="downtime_7d", device_class=SensorDeviceClass.DURATION,
             native_unit_of_measurement=UnitOfTime.SECONDS, suggested_unit_of_measurement=UnitOfTime.MINUTES,
             state_class=SensorStateClass.MEASUREMENT, value=lambda h: h.outage_stats()["downtime_7d"]),
    HLSensor(key="availability_7d", native_unit_of_measurement=PERCENTAGE, suggested_display_precision=2,
             state_class=SensorStateClass.MEASUREMENT, icon="mdi:percent-circle-outline",
             value=lambda h: h.outage_stats()["availability_7d"]),
    HLSensor(key="availability_30d", native_unit_of_measurement=PERCENTAGE, suggested_display_precision=2,
             state_class=SensorStateClass.MEASUREMENT, icon="mdi:percent-circle-outline",
             value=lambda h: h.outage_stats()["availability_30d"]),
    HLSensor(key="last_outage", device_class=SensorDeviceClass.TIMESTAMP, icon="mdi:lan-disconnect",
             value=lambda h: _ts((h.log.outages[-1] if h.log.outages else {}).get("start")),
             attrs=lambda h: {"duration": (h.log.outages[-1]["duration"] if h.log.outages else None),
                              "cause": (h.log.outages[-1]["cause"] if h.log.outages else None),
                              "recent_outages": h.log.recent()}),
    HLSensor(key="last_outage_duration", device_class=SensorDeviceClass.DURATION,
             native_unit_of_measurement=UnitOfTime.SECONDS, suggested_unit_of_measurement=UnitOfTime.MINUTES,
             icon="mdi:timer-alert-outline",
             value=lambda h: h.log.outages[-1]["duration"] if h.log.outages else None),
    HLSensor(key="last_check", device_class=SensorDeviceClass.TIMESTAMP, icon="mdi:clock-check-outline",
             entity_category=EntityCategory.DIAGNOSTIC, value=lambda h: h.last_check),
    # Neueinwahl
    HLSensor(key="wan_ip", icon="mdi:ip-network", entity_category=EntityCategory.DIAGNOSTIC,
             value=lambda h: h.data["reconnect"].get("ip"),
             attrs=lambda h: {"previous_ip": h.data["reconnect"].get("old_ip")}),
    HLSensor(key="last_reconnect", device_class=SensorDeviceClass.TIMESTAMP, icon="mdi:restart",
             value=lambda h: _ts(h.data["reconnect"].get("last"))),
    HLSensor(key="reconnect_result", device_class=SensorDeviceClass.ENUM, icon="mdi:check-network",
             options=["ok_new_ip", "ok_same_ip", "no_effect", "error", "triggered"],
             value=lambda h: h.data["reconnect"].get("result"),
             attrs=lambda h: {"error": h.data["reconnect"].get("error"), "last": h.data["reconnect"].get("last"),
                              "method": h.opt("reconnect_method", "pppd_hup"),
                              "enabled": h.reconnect_enabled, "time": h.reconnect_time.strftime("%H:%M")}),
]


async def async_setup_entry(hass, entry, async_add_entities):
    hub: HomeLinesHub = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(HomeLinesSensor(hub, d) for d in SENSORS)


class HomeLinesSensor(HomeLinesEntity, SensorEntity):
    _lg_domain = "sensor"
    entity_description: HLSensor

    def __init__(self, hub: HomeLinesHub, desc: HLSensor) -> None:
        super().__init__(hub, desc.key)
        self.entity_description = desc

    @property
    def native_value(self):
        return self.entity_description.value(self.hub)

    @property
    def extra_state_attributes(self):
        if self.entity_description.attrs:
            return self.entity_description.attrs(self.hub)
        return None
