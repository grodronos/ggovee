"""Base entity for Govee devices."""

from homeassistant.helpers.entity import Entity
from .const import DOMAIN, MANUFACTURER


class GoveeEntity(Entity):
    """Base class for Govee entities."""

    def __init__(self, coordinator, config_entry, device):
        """Initialize the GoveeEntity."""
        self.coordinator = coordinator
        self.config_entry = config_entry
        self.device = device

        # Nastavíme jedinečné ID.
        # Předpokládejme, že `device` je dict s klíčem "device",
        # který obsahuje unikátní string pro identifikaci daného Govee zařízení.
        self._attr_unique_id = device["device"]

        # Volitelné - nastavení informací o zařízení v HA
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device["device"])},
            "manufacturer": MANUFACTURER,
            "name": device.get("deviceName", "Govee Device"),
        }

    @property
    def name(self):
        """Return the default name for this entity."""
        return self.device.get("deviceName", "Govee Unknown")

    @property
    def available(self):
        """Return True if coordinator update was successful."""
        return self.coordinator.last_update_success

    async def async_update(self):
        """Request an update from the coordinator."""
        await self.coordinator.async_request_refresh()
