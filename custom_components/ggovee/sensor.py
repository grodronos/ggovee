import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Nastavení senzorů z konfiguračního záznamu."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    sensors = []

    for device in coordinator.data:
        if device["model"] == "H5179":
            sensors.append(GoveeTemperatureSensor(coordinator, device))
            sensors.append(GoveeHumiditySensor(coordinator, device))

    async_add_entities(sensors, update_before_add=True)

class GoveeTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Reprezentace teplotního senzoru Govee."""

    def __init__(self, coordinator, device):
        """Inicializace senzoru."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device['device_name']} Teplota"
        self._attr_unique_id = f"{device['device']}_temperature"
        self._attr_unit_of_measurement = TEMP_CELSIUS
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device["device"])},
            "name": device["device_name"],
            "manufacturer": "Govee",
            "model": device["model"],
        }

    @property
    def state(self):
        """Vrátí aktuální teplotu."""
        return self._device["temperature"]

class GoveeHumiditySensor(CoordinatorEntity, SensorEntity):
    """Reprezentace vlhkostního senzoru Govee."""

    def __init__(self, coordinator, device):
        """Inicializace senzoru."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device['device_name']} Vlhkost"
        self._attr_unique_id = f"{device['device']}_humidity"
        self._attr_unit_of_measurement = PERCENTAGE
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device["device"])},
            "name": device["device_name"],
            "manufacturer":
::contentReference[oaicite:0]{index=0}
 
