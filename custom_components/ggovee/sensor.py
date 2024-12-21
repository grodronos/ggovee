"""Platforma senzoru pro ggovee."""
from __future__ import annotations

from datetime import timedelta
import logging

from govee_api_laggat import Govee
from govee_api_laggat.govee_dtos import GoveeDevice

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    TEMP_CELSIUS,
    LIGHT_LUX,
    ELECTRIC_POTENTIAL_VOLT,
    ELECTRIC_CURRENT_AMPERE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GoveeDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="temperature",
        name="Teplota",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
    SensorEntityDescription(
        key="humidity",
        name="Vlhkost",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        key="battery",
        name="Baterie",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        key="illuminance",
        name="Osvětlení",
        device_class=SensorDeviceClass.ILLUMINANCE,
        native_unit_of_measurement=LIGHT_LUX,
    ),
    SensorEntityDescription(
        key="voltage",
        name="Napětí",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
    ),
    SensorEntityDescription(
        key="current",
        name="Proud",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
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
        GoveeSensor(coordinator, device, description)
        for device in coordinator.data
        for description in SENSOR_TYPES
        if description.key in device.sensors
    )

class GoveeSensor(CoordinatorEntity[GoveeDataUpdateCoordinator], SensorEntity):
    """Reprezentace senzoru Govee."""

    def __init__(
        self,
        coordinator: GoveeDataUpdateCoordinator,
        device: GoveeDevice,
        description: SensorEntityDescription,
    ) -> None:
        """Inicializace senzoru."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device = device
        self._attr_unique_id = f"{device.device}-{description.key}"
        self._attr_name = f"{device.device_name} {description.name}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device.device)},
            "name": device.device_name,
            "manufacturer": "Govee",
            "model": device.model,
        }

    @property
    def native_value(self):
        """Vrátí stav senzoru."""
        return self._device.sensors.get(self.entity_description.key)
