"""Platform for sensor integration."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Nové importy pro jednotky
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
)

from .const import DOMAIN
from .entity import GoveeEntity
from .coordinator import GoveeDataUpdateCoordinator


@dataclass
class GoveeSensorEntityDescription(SensorEntityDescription):
    """Describes Govee sensor entity."""


SENSORS: tuple[GoveeSensorEntityDescription, ...] = (
    GoveeSensorEntityDescription(
        key="temp",
        translation_key="temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GoveeSensorEntityDescription(
        key="hum",
        translation_key="humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GoveeSensorEntityDescription(
        key="battery",
        translation_key="battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GoveeSensorEntityDescription(
        key="voltage",
        translation_key="voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    GoveeSensorEntityDescription(
        key="current",
        translation_key="current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up Govee sensor platform."""
    # Získáme data uložená při async_setup_entry v __init__.py
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Tady by mělo být "coordinator" typu GoveeDataUpdateCoordinator
    coordinator: GoveeDataUpdateCoordinator = entry_data["coordinator"]

    # Například "device" může být nějaký další parametr
    device = entry_data["device"]

    # Pokud coordinator ještě nemá žádná nasbíraná data, tak rovnou končíme
    if not coordinator.data:
        return

    sensors = []

    # coordinator.data by mělo být dictionary (např. { "MAC_adresa": {...}, ... })
    for dev_id, dev_info in coordinator.data.items():
        for sensor_description in SENSORS:
            # "dev_info" je nějaký slovník s klíčem "data", což opět bývá dict naměřených hodnot
            if sensor_description.key in dev_info["data"]:
                sensors.append(
                    GoveeSensorEntity(
                        coordinator=coordinator,
                        device=dev_id,  # Předáme identifikátor zařízení
                        description=sensor_description,
                    )
                )

    async_add_entities(sensors)


class GoveeSensorEntity(GoveeEntity, SensorEntity):
    """Representation of Govee Sensor."""

    entity_description: GoveeSensorEntityDescription

    def __init__(
        self,
        coordinator: GoveeDataUpdateCoordinator,
        device: str,
        description: GoveeSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self.entity_description = description

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        # Získáme konkrétní měřenou hodnotu podle klíče (např. "temp", "hum" atd.)
        sensor_value = self.coordinator.data[self._device]["data"].get(
            self.entity_description.key
        )
        if sensor_value is not None:
            return round(sensor_value, 2)
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
