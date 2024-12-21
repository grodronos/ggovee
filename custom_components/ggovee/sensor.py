"""Platforma pro senzory Govee BLE v Home Assistant."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    TEMP_CELSIUS,
    UnitOfTemperature,
    UnitOfHumidity,
    UnitOfLight,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import GoveeBleDeviceDataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="temperature",
        name="Teplota",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="humidity",
        name="Vlhkost",
        native_unit_of_measurement=UnitOfHumidity.PERCENT,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="battery",
        name="Baterie",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Nastavení platformy sensorů."""
    coordinator: GoveeBleDeviceDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        GoveeTemperatureHumiditySensor(coordinator, description)
        for description in SENSOR_TYPES
        if description.key in coordinator.data
    )


class GoveeTemperatureHumiditySensor(
    CoordinatorEntity[GoveeBleDeviceDataUpdateCoordinator], SensorEntity
):
    """Reprezentace senzoru teploty a vlhkosti Govee BLE."""

    def __init__(
        self,
        coordinator: GoveeBleDeviceDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Inicializace senzoru."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.address}-{description.key}"
        self._attr_name = f"{coordinator.name} {description.name}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": self._attr_name,
            "manufacturer": "Govee",
        }

    @property
    def native_value(self):
        """Vrátí stav senzoru."""
        return self.coordinator.data.get(self.entity_description.key)
