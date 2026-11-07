"""Binary sensors for City of Logan."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import  LoganCoordinator
from .const import DOMAIN,  MODE_WASTE
from .waste import put_out_tonight


class LoganWastePutOutTonightSensor(
    CoordinatorEntity[LoganCoordinator], BinarySensorEntity
):
    """True when bins go out tonight for tomorrow's collection."""

    _attr_has_entity_name = True
    _attr_name = "Put bins out tonight"
    _attr_unique_id = "logan_waste_put_out_tonight"

    def __init__(self, coordinator: LoganCoordinator) -> None:
        """Initialise the binary sensor."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            name="Logan",
            manufacturer="belikh",
            model="Logan Integration",
            configuration_url="https://github.com/belikh/ha-logan",
        )

    @property
    def is_on(self) -> bool:
        """Return whether bins go out tonight."""
        waste = self.coordinator.waste or {}
        bin_day = str(waste.get("Collection_Day") or "")
        try:
            from zoneinfo import ZoneInfo

            today = datetime.now(ZoneInfo("Australia/Brisbane")).date()
        except Exception:  # noqa: BLE001 - fallback to UTC date
            today = datetime.now().date()
        return put_out_tonight(bin_day, today)

    @property
    def extra_state_attributes(self) -> dict:
        """Return waste details."""
        waste = self.coordinator.waste or {}
        return {
            "address": waste.get("Formatted_Property_Address"),
            "bin_day": waste.get("Collection_Day"),
            "recycle_week": waste.get("Recycling_Week"),
        }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Logan binary sensors from a config entry."""
    coordinator: LoganCoordinator = hass.data["logan"][entry.entry_id]
    if coordinator.mode != MODE_WASTE:
        return
    async_add_entities([LoganWastePutOutTonightSensor(coordinator)])
