"""Sensors for City of Logan."""

from __future__ import annotations

from datetime import UTC, date, datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import  LoganCoordinator
from .const import DOMAIN,  MODE_NEARBY, MODE_WASTE
from .waste import next_collection_date

EPOCH = date(2026, 1, 5)


class LoganLayerSensor(CoordinatorEntity[LoganCoordinator], SensorEntity):
    """Sensor exposing the feature count for one Datahub layer."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LoganCoordinator,
        layer_title: str,
        source_url: str,
    ) -> None:
        """Initialise with the layer title and source URL."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            name="Logan",
            manufacturer="belikh",
            model="Logan Integration",
            configuration_url="https://github.com/belikh/ha-logan",
        )
        self._layer_title = layer_title
        self._source_url = source_url
        slug = layer_title.lower().replace(" ", "_")
        self._attr_unique_id = f"{layer_title}_{slug}"
        self._attr_name = layer_title
        self._attr_native_unit_of_measurement = "features"

    @property
    def native_value(self) -> int | None:
        """Return the feature count for this layer."""
        return self.coordinator.counts.get(self._layer_title)

    @property
    def extra_state_attributes(self) -> dict:
        """Return layer metadata."""
        return {
            "layer_title": self._layer_title,
            "source_url": self._source_url,
            "feature_count": self.coordinator.counts.get(self._layer_title),
        }


class LoganWasteNextCollectionSensor(CoordinatorEntity[LoganCoordinator], SensorEntity):
    """Sensor for the next bin collection date."""

    _attr_has_entity_name = True
    _attr_device_class = None
    _attr_name = "Next bin collection"
    _attr_unique_id = "logan_waste_next_collection"

    def __init__(self, coordinator: LoganCoordinator) -> None:
        """Initialise the waste sensor."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            name="Logan",
            manufacturer="belikh",
            model="Logan Integration",
            configuration_url="https://github.com/belikh/ha-logan",
        )

    @property
    def native_value(self) -> str | None:
        """Return the next collection date as ISO text."""
        waste = self.coordinator.waste or {}
        bin_day = str(waste.get("Collection_Day") or "")
        today = datetime.now(UTC).date()
        try:
            from zoneinfo import ZoneInfo

            today = datetime.now(ZoneInfo("Australia/Brisbane")).date()
        except Exception:  # noqa: BLE001 - fallback to UTC date
            pass
        nxt = next_collection_date(bin_day, today)
        return nxt.isoformat() if nxt else None

    @property
    def extra_state_attributes(self) -> dict:
        """Return waste details."""
        waste = self.coordinator.waste or {}
        return {
            "address": waste.get("Formatted_Property_Address"),
            "bin_day": waste.get("Collection_Day"),
            "recycle_week": waste.get("Recycling_Week"),
            "suburb": waste.get("Suburb"),
        }


class LoganDevAppStatusSensor(CoordinatorEntity[LoganCoordinator], SensorEntity):
    """Status of the nearest undecided development application."""

    _attr_has_entity_name = True
    _attr_name = "Development application (nearest)"
    _attr_unique_id = "logan_dev_app_status"

    def __init__(self, coordinator: LoganCoordinator) -> None:
        """Initialise the status sensor."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            name="Logan",
            manufacturer="belikh",
            model="Logan Integration",
            configuration_url="https://github.com/belikh/ha-logan",
        )

    @property
    def native_value(self) -> str | None:
        """Return the status of the nearest application."""
        nearby = self.coordinator.nearby
        if not nearby:
            return "None nearby"
        return "Under assessment"

    @property
    def extra_state_attributes(self) -> dict:
        """Return nearby application details."""
        nearby = self.coordinator.nearby
        if not nearby:
            return {"count": 0, "radius_km": self.coordinator.radius_km}
        return {
            "count": len(nearby),
            "radius_km": self.coordinator.radius_km,
            "distance_km": nearby[0].get("distance_km"),
        }


class LoganRoadBlockStatusSensor(CoordinatorEntity[LoganCoordinator], SensorEntity):
    """Status of the nearest road block."""

    _attr_has_entity_name = True
    _attr_name = "Road block (nearest)"
    _attr_unique_id = "logan_road_block_status"

    def __init__(self, coordinator: LoganCoordinator) -> None:
        """Initialise the status sensor."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, DOMAIN)},
            name="Logan",
            manufacturer="belikh",
            model="Logan Integration",
            configuration_url="https://github.com/belikh/ha-logan",
        )

    @property
    def native_value(self) -> str | None:
        """Return the nearest road block status."""
        blocks = self.coordinator.road_blocks
        if not blocks:
            return "None nearby"
        return "Active"

    @property
    def extra_state_attributes(self) -> dict:
        """Return nearby block details."""
        blocks = self.coordinator.road_blocks
        if not blocks:
            return {"radius_km": self.coordinator.radius_km}
        return {
            "radius_km": self.coordinator.radius_km,
            "distance_km": blocks[0].get("distance_km"),
        }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Logan sensors from a config entry."""
    coordinator: LoganCoordinator = hass.data["logan"][entry.entry_id]
    entities: list[SensorEntity] = []
    for layer in coordinator.layers:
        entities.append(LoganLayerSensor(coordinator, layer.title, layer.url))
    if coordinator.mode == MODE_WASTE:
        entities.append(LoganWasteNextCollectionSensor(coordinator))
    if coordinator.mode == MODE_NEARBY:
        entities.append(LoganDevAppStatusSensor(coordinator))
        entities.append(LoganRoadBlockStatusSensor(coordinator))
    async_add_entities(entities)
