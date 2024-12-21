import requests
import logging

_LOGGER = logging.getLogger(__name__)

class GoveeApiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://developer-api.govee.com/v1"
        self.headers = {
            "Govee-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def get_devices(self):
        url = f"{self.base_url}/devices"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("data", {}).get("devices", [])
        else:
            _LOGGER.error("Failed to fetch devices: %s", response.text)
            return []

    def get_device_state(self, device):
        url = f"{self.base_url}/devices/state"
        params = {"device": device["device"], "model": device["model"]}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", {}).get("properties", [])
        else:
            _LOGGER.error("Failed to fetch device state for %s: %s", device["device"], response.text)
            return []

    def update_devices(self):
        devices = self.get_devices()
        for device in devices:
            state = self.get_device_state(device)
            device.update(state)
        return devices
