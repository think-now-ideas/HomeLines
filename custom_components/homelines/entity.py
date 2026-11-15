"""Basisklasse für HomeLines-Entitäten."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, NAME, SIGNAL_UPDATE, VERSION
from .hub import HomeLinesHub


class HomeLinesEntity(Entity):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, hub: HomeLinesHub, key: str) -> None:
        self.hub = hub
        self._attr_translation_key = key
        self._attr_unique_id = f"{hub.entry.entry_id}_{key}"
        if getattr(self, "_lg_domain", None):
            # Feste, sprachunabhängige IDs, z. B. sensor.homelines_outages_24h
            self.entity_id = f"{self._lg_domain}.homelines_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, hub.entry.entry_id)},
            name=hub.entry.title, manufacturer=NAME, model="Internet Monitor & Mobile Failover",
            sw_version=VERSION)

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(async_dispatcher_connect(
            self.hass, SIGNAL_UPDATE.format(self.hub.entry.entry_id), self.async_write_ha_state))
