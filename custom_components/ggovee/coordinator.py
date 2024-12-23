import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class GoveeDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api):
        """Inicializace koordinátoru."""
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name="Govee",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Aktualizace dat prostřednictvím API."""
        try:
            data = await self.api.get_data()
            return data
        except Exception as err:
            raise UpdateFailed(f"Chyba při aktualizaci dat: {err}")