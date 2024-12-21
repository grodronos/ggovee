"""Platforma senzoru pro ggovee."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    TEMP_CELSIUS,
    UnitOfTemperature,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import GoveeDataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="temperature",
        name="Teplota",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    SensorEntityDescription(
        key="humidity",
        name="Vlhkost",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        key="battery",
        name="Baterie",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        key="energy",
        name="Spotřeba energie",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="power",
        name="Výkon",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Nastavení platformy senzoru."""
    coordinator: GoveeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        GoveeSensor(coordinator, description) for description in SENSOR_TYPES
    )

class GoveeSensor(CoordinatorEntity[GoveeDataUpdateCoordinator], SensorEntity):
    """Reprezentace senzoru Govee."""

    def __init__(
        self,
        coordinator: GoveeDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Inicializace senzoru."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.mac_address}_{description.key}"

    @property
    def native_value(self):
        """Vrátí sta
