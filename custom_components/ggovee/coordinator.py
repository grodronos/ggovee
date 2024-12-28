from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .GoveeApi.UserDevices.user_devices_controller import UserDevicesController
from .GoveeApi.UserDevices.models import Device
from .GoveeApi.DeviceState.device_state_controller import DeviceStateController
from .const import DOMAIN, API_KEY, UPDATE_INTERVAL
from .GoveeApi.DeviceState.models import Capability, State, CapabilityProcessor
import logging
import json
import os
import aiofiles

logger = logging.getLogger(__name__)

async def get_translations(hass, domain):
    lang = hass.config.language
    result = await load_translation(hass, domain, lang)
    if not result:
        logger.warning(f"Překlad pro jazyk '{lang}' nebyl nalezen. Načítám anglický překlad.")
        result = await load_translation(hass, domain, "en")
    return result

async def load_translation(hass, domain, lang):
    translation_file = os.path.join(
        os.path.dirname(__file__),
        "translations",
        f"{lang}.json"
    )

    if os.path.isfile(translation_file):
        try:
            async with aiofiles.open(translation_file, "r", encoding="utf-8") as f:
                content = await f.read()
            return json.loads(content)
        except FileNotFoundError:
            logger.warning(f"Překladový soubor nebyl nalezen: {translation_file}")
        except json.JSONDecodeError as e:
            logger.error(f"Chyba při dekódování JSON z {translation_file}: {e}")
        except Exception as e:
            logger.error(f"Neočekávaná chyba při načítání překladového souboru {translation_file}: {e}")
    else:
        logger.warning(f"Překladový soubor neexistuje: {translation_file}")
    
    return None

class Coordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self.api_key = entry.data.get(API_KEY, None)
        self.processor = CapabilityProcessor()

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
                self.translations = await get_translations(self.hass, DOMAIN)
                self.userDevicesController = UserDevicesController(api_key=self.api_key)
                self.deviceStateController = DeviceStateController(api_key=self.api_key)
                try:
                    data = await self.userDevicesController.getDevices(self.hass)
                    self.data["devices"] = {}
                    self.data["sensors"] = {}
                    for device in data:
                        self.data["devices"][device.device] = device
                        self.data["sensors"][device.device] = {}
                        for capability in device.capabilities:
                            self.data["sensors"][device.device][capability.instance] = {}
                            self.data["sensors"][device.device][capability.instance]["unit"] = self.translations["sensor"][capability.instance]["unit"]
                            self.data["sensors"][device.device][capability.instance]["name"] = self.translations["sensor"][capability.instance]["name"]
                            self.data["sensors"][device.device][capability.instance]["unique_id"] = (f"{device.device}_{capability.instance}").replace(":", "_").lower()
                            self.data["sensors"][device.device][capability.instance]["value"] = 0
                except Exception as e:
                    logger.error("Chyba: %s", str(e))

            for deviceId, device in self.data["devices"].items():
                capabilities = await self.deviceStateController.getDeviceState(self.hass, device)
                for capability in capabilities:
                    if capability.instance in self.data["sensors"][deviceId]:
                        newValue = self.processor.process(capability.instance, capability.state.value)
                        oldValue = self.data["sensors"][deviceId][capability.instance]["value"]
                        if newValue != oldValue:
                            self.hass.bus.async_fire(
                                "logbook_entry",
                                {
                                    "message": f"{self.data["devices"][deviceId].deviceName}: {newValue}{self.data["sensors"][deviceId][capability.instance]["unit"]}",
                                    "domain": "sensor",
                                    "entity_id": self.data["sensors"][deviceId][capability.instance].get("entity_id", f"sensor.{self.data["sensors"][deviceId][capability.instance]["name"]}"),
                                },
                            )
                        self.data["sensors"][deviceId][capability.instance]["value"] = newValue
            return self.data

        except Exception as e:
            logger.error("Chyba při načítání dat: %s", e)
            raise UpdateFailed(f"Chyba při načítání dat: {e}") from e