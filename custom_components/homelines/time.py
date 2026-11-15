"""Uhrzeit der täglichen Neueinwahl."""

from __future__ import annotations

from datetime import time

from homeassistant.components.time import TimeEntity

from .const import DOMAIN
from .entity import HomeLinesEntity
from .hub import HomeLinesHub


async def async_setup_entry(hass, entry, async_add_entities):
    hub: HomeLinesHub = hass.data[DOMAIN][entry.entry_id]
    if hub.reconnect_configured:
        async_add_entities([ReconnectTime(hub)])


class ReconnectTime(HomeLinesEntity, TimeEntity):
    _lg_domain = "time"
    _attr_icon = "mdi:clock-outline"

    def __init__(self, hub):
        super().__init__(hub, "reconnect_time")

    @property
    def native_value(self) -> time:
        return self.hub.reconnect_time

    async def async_set_value(self, value: time) -> None:
        await self.hub.async_set_reconnect(at=value)
