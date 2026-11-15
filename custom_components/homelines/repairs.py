"""Reparatur-Dialog: neuen SSH-Fingerabdruck des Routers übernehmen."""

from __future__ import annotations

from homeassistant import data_entry_flow
from homeassistant.components.repairs import RepairsFlow
from homeassistant.core import HomeAssistant

from .const import DOMAIN


class HostKeyFlow(RepairsFlow):
    """Bestätigen, dass der Router mit dem neuen Fingerabdruck wirklich der eigene ist."""

    def __init__(self, entry_id: str) -> None:
        self.entry_id = entry_id

    def _hub(self):
        return self.hass.data.get(DOMAIN, {}).get(self.entry_id)

    async def async_step_init(self, user_input=None) -> data_entry_flow.FlowResult:
        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None) -> data_entry_flow.FlowResult:
        hub = self._hub()
        if hub is None:
            return self.async_abort(reason="not_loaded")
        if user_input is not None:
            await hub.async_accept_host_key()
            return self.async_create_entry(data={})
        pend = hub.ssh_pending() or {}
        return self.async_show_form(step_id="confirm", description_placeholders={
            "old": (hub.data.get("ssh") or {}).get("fingerprint") or "–",
            "new": pend.get("fingerprint") or "nicht lesbar",
        })


async def async_create_fix_flow(hass: HomeAssistant, issue_id: str, data: dict | None) -> RepairsFlow:
    return HostKeyFlow((data or {}).get("entry_id", ""))
