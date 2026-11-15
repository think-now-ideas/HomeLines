"""Binärsensoren von HomeLines."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity

from .const import DOMAIN, MODE_NORMAL
from .entity import HomeLinesEntity
from .hub import HomeLinesHub


async def async_setup_entry(hass, entry, async_add_entities):
    hub: HomeLinesHub = hass.data[DOMAIN][entry.entry_id]
    ents = [
        HLBinary(hub, "internet", BinarySensorDeviceClass.CONNECTIVITY, lambda h: h.internet,
                 lambda h: {"current_outage": h.log.current}),
        HLBinary(hub, "emergency", BinarySensorDeviceClass.PROBLEM, lambda h: h.mode != MODE_NORMAL),
        HLBinary(hub, "phone", BinarySensorDeviceClass.CONNECTIVITY,
                 lambda h: h.phone()["reporting"] if h.phone()["configured"] else None,
                 lambda h: h.phone()),
        HLBinary(hub, "router_link", BinarySensorDeviceClass.PROBLEM, lambda h: h.router_error is not None,
                 lambda h: {"error": h.router_error}),
    ]
    if hub.router_ip:
        ents.append(HLBinary(hub, "router", BinarySensorDeviceClass.CONNECTIVITY, lambda h: h.router_ok))
    async_add_entities(ents)


class HLBinary(HomeLinesEntity, BinarySensorEntity):
    _lg_domain = "binary_sensor"
    def __init__(self, hub, key, device_class, value, attrs=None):
        super().__init__(hub, key)
        self._attr_device_class = device_class
        self._value, self._attrs = value, attrs

    @property
    def is_on(self):
        return self._value(self.hub)

    @property
    def extra_state_attributes(self):
        return self._attrs(self.hub) if self._attrs else None
