import aiohttp
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

    async def get_devices(self):
        url = f"{self.base_url}/devices"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", {}).get("devices", [])
                else:
                    _LOGGER.error("Failed to fetch devices: %s", await response.text())
                    return []

    async def get_device_state(self, device):
        url = f"{self.base_url}/devices/state"
        params = {"device": device["device"], "model": device["model"]}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", {}).get("properties", [])
                else:
                    _LOGGER.error("Failed to fetch device state for %s: %s", device["device"], await response.text())
                    return []

    async def update_devices(self):
        devices = await self.get_devices()
        for device in devices:
            state = await self.get_device_state(device)
            device.update(state)
        return devices
