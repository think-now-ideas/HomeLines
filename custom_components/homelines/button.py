"""Buttons von HomeLines."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .entity import HomeLinesEntity
from .hub import FlatError, HomeLinesHub


async def async_setup_entry(hass, entry, async_add_entities):
    hub: HomeLinesHub = hass.data[DOMAIN][entry.entry_id]
    ents = [HLButton(hub, "activate_dayflat", "mdi:lock-open-variant", _flat),
            HLButton(hub, "restrict", "mdi:lock", lambda h: h.async_restrict()),
            HLButton(hub, "reset_usage", "mdi:counter", lambda h: h.async_reset_usage()),
            HLButton(hub, "test_notify", "mdi:message-badge-outline", lambda h: h.async_test_notify())]
    if hub.reconnect_configured:
        ents.append(HLButton(hub, "reconnect_now", "mdi:restart", lambda h: h.async_reconnect()))
    async_add_entities(ents)


async def _flat(hub: HomeLinesHub):
    try:
        await hub.async_activate_flat()
    except FlatError as err:
        raise HomeAssistantError(translation_domain=DOMAIN, translation_key=err.args[0]) from err


class HLButton(HomeLinesEntity, ButtonEntity):
    _lg_domain = "button"
    def __init__(self, hub, key, icon, action):
        super().__init__(hub, key)
        self._attr_icon = icon
        self._action = action

    async def async_press(self) -> None:
        await self._action(self.hub)
