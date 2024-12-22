"""DataUpdateCoordinator for Govee Bluetooth."""
from __future__ import annotations

import logging
import asyncio

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import async_timeout

from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

class GoveeDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Govee data."""

    def __init__(self, hass: HomeAssistant, config_entry):
        """Initialize."""
        self.hass = hass
        self.entry = config_entry
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}-{config_entry.entry_id}",
            update_interval=None,  # Nebo interval, pokud potřebujete pravidelné scanování
        )

    async def _async_update_data(self):
        """Update data via library (BLE or other)."""
        _LOGGER.info("GoveeDataUpdateCoordinator:_async_update_data")