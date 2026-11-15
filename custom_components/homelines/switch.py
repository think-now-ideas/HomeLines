"""Schalter: tägliche Neueinwahl."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .entity import HomeLinesEntity
from .hub import HomeLinesHub


async def async_setup_entry(hass, entry, async_add_entities):
    hub: HomeLinesHub = hass.data[DOMAIN][entry.entry_id]
    if hub.reconnect_configured:
        async_add_entities([ReconnectSwitch(hub)])


class ReconnectSwitch(HomeLinesEntity, SwitchEntity):
    _lg_domain = "switch"
    _attr_icon = "mdi:calendar-sync"

    def __init__(self, hub):
        super().__init__(hub, "daily_reconnect")

    @property
    def is_on(self):
        return self.hub.reconnect_enabled

    async def async_turn_on(self, **kwargs):
        await self.hub.async_set_reconnect(enabled=True)

    async def async_turn_off(self, **kwargs):
        await self.hub.async_set_reconnect(enabled=False)
