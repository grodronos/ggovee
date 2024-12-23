from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .GoveeApi.UserDevices.user_devices_controller import UserDevicesController
from .GoveeApi.UserDevices.models import Device
from .const import DOMAIN, API_KEY, UPDATE_INTERVAL
import aiohttp
import logging

logger = logging.getLogger(__name__)

class Coordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self.api_key = entry.data.get(API_KEY, None)

        super().__init__(
            hass,
            logger,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):
        try:
            if not self.data:
                self.data = {}
                logger.debug("První načtení dat: seznam zařízení a jejich stavy")
                userDevicesController = UserDevicesController(api_key=self.api_key)
                try:
                    data = await userDevicesController.getDevices(self.hass)
                    self.data["devices"] = {}
                    self.data["statuses"] = {}
                    logger.debug("Získáno zařízení: %s", str(len(data)))
                    for device in data:
                        logger.debug("Zařízení: %s (%s)", str(device.deviceName), str(device.device))
                        self.data["devices"][device.device] = device
                        self.data["statuses"][device.device] = {}
                        for capability in device.capabilities:
                            logger.debug("  - %s", str(capability.instance))
                            self.data["statuses"][device.device][capability.instance] = {}
                            self.data["statuses"][device.device][capability.instance]["unit"] = "teplota"
                            self.data["statuses"][device.device][capability.instance]["value"] = 0
                except Exception as e:
                    logger.error("Chyba: %s", str(e))

            logger.debug("Aktualizace dat")
            #self.statuses = await self.fetch_statuses()

            # Aktualizace stavů senzorů ve stávajících zařízeních
            #for device in data.get("devices", []):
            #    device_id = device.get("id")
            #    if device_id in statuses:
            #        for sensor in device.get("sensors", []):
            #            sensor_id = sensor.get("id")
            #            if sensor_id in statuses[device_id]:
            #                sensor["state"] = statuses[device_id][sensor_id]["state"]
            #                sensor["unit"] = statuses[device_id][sensor_id]["unit"]

            #logger.debug("Aktualizovaná data: %s", data)
            return self.data

        except Exception as e:
            logger.error("Chyba při načítání dat: %s", e)
            raise UpdateFailed(f"Chyba při načítání dat: {e}") from e