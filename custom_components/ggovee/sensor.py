import logging
import requests
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS

from .const import DOMAIN, API_URL

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Nastavení platformy senzoru."""
    api_key = hass.data[DOMAIN].get("api_key")
    devices = get_govee_devices(api_key)
    sensors = []
    for device in devices:
        if device["model"] == "H5179":
            sensors.append(GoveeTemperatureSensor(device, api_key))
            sensors.append(GoveeHumiditySensor(device, api_key))
    add_entities(sensors, True)

def get_govee_devices(api_key):
    """Získání seznamu zařízení z Govee API."""
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", {}).get("devices", [])
    else:
        _LOGGER.error("Chyba při získávání zařízení: %s", response.text)
        return []

class GoveeTemperatureSensor(SensorEntity):
    """Reprezentace teplotního senzoru Govee H5179."""

    def __init__(self, device, api_key):
        self._device = device
        self._api_key = api_key
        self._name = f"{device['deviceName']} Teplota"
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    def update(self):
        """Aktualizace stavu senzoru."""
        data = self.get_device_data()
        if data:
            self._state = data.get("temperature")

    def get_device_data(self):
        """Získání dat zařízení z Govee API."""
        headers = {"Authorization": f"Bearer {self._api_key}"}
        response = requests.get(f"{API_URL}/{self._device['device']}/state", headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            _LOGGER.error("Chyba při získávání dat zařízení: %s", response.text)
            return None

class GoveeHumiditySensor(SensorEntity):
    """Reprezentace vlhkostního senzoru Govee H5179."""

    def __init__(self, device, api_key):
        self._device = device
        self._api_key = api_key
        self._name = f"{device['deviceName']} Vlhkost"
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "%"

    def update(self):
        """Aktualizace stavu senzoru."""
        data = self.get_device_data()
        if data:
            self._state = data.get("humidity")

    def get_device_data(self):
        """Získání dat zařízení z Govee API."""
        headers = {"Authorization": f"Bearer {self._api_key}"}
        response = requests.get(f"{API_URL}/{self._device['device']}/state", headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            _LOGGER.error("Chyba při získávání dat zařízení: %s", response.text)
            return None