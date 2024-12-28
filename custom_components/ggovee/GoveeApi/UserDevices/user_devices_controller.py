# GoveeApi/UserDevices/controller.py
# Response JSON: {'code': 200, 'message': 'success', 'data': [{'sku': 'H5179', 'device': '59:7C:1F:64:04:40:EC:83', 'deviceName': 'Domek', 'type': 'devices.types.thermometer', 'capabilities': [{'type': 'devices.capabilities.property', 'instance': 'sensorTemperature'}, {'type': 'devices.capabilities.property', 'instance': 'sensorHumidity'}]}, {'sku': 'H5179', 'device': 'E4:EC:1F:64:04:42:74:56', 'deviceName': 'Dům1', 'type': 'devices.types.thermometer', 'capabilities': [{'type': 'devices.capabilities.property', 'instance': 'sensorTemperature'}, {'type': 'devices.capabilities.property', 'instance': 'sensorHumidity'}]}, {'sku': 'H5179', 'device': 'C5:1F:1F:64:04:40:AC:89', 'deviceName': 'Garáž', 'type': 'devices.types.thermometer', 'capabilities': [{'type': 'devices.capabilities.property', 'instance': 'sensorTemperature'}, {'type': 'devices.capabilities.property', 'instance': 'sensorHumidity'}]}, {'sku': 'H5179', 'device': 'BB:AA:1F:64:04:43:3C:B2', 'deviceName': 'Dům2', 'type': 'devices.types.thermometer', 'capabilities': [{'type': 'devices.capabilities.property', 'instance': 'sensorTemperature'}, {'type': 'devices.capabilities.property', 'instance': 'sensorHumidity'}]}, {'sku': 'H5179', 'device': 'BB:AA:1F:64:04:43:34:2A', 'deviceName': 'Půda', 'type': 'devices.types.thermometer', 'capabilities': [{'type': 'devices.capabilities.property', 'instance': 'sensorTemperature'}, {'type': 'devices.capabilities.property', 'instance': 'sensorHumidity'}]}, {'sku': 'H5179', 'device': 'BB:AA:1F:64:04:41:D8:EF', 'deviceName': 'Venku', 'type': 'devices.types.thermometer', 'capabilities': [{'type': 'devices.capabilities.property', 'instance': 'sensorTemperature'}, {'type': 'devices.capabilities.property', 'instance': 'sensorHumidity'}]}]}

import requests
from typing import List, Dict
from .models import Response, Device
import logging

logger = logging.getLogger(__name__)

class UserDevicesController:
    def __init__(self, api_key: str, timeout: int = 10):
        self.base_url = "https://openapi.api.govee.com/router/api/v1"
        self.timeout = timeout
        self.headers={
            "Content-Type":"application/json",
            "Govee-API-Key": api_key
        }

    async def getDevices(self, hass) -> List[Device]:
        path = 'user/devices'
        url = f"{self.base_url}/{path.strip('/')}"

        try:
            request_func = lambda: requests.get(url, headers=self.headers, timeout=self.timeout)
            response = await hass.async_add_executor_job(request_func)
            if response.status_code != 200:
                logger.error(f"HTTP Error: {response.status_code} - {response.text}")
                response.raise_for_status()

            response_json = response.json()
            api_response = self.parse_api_response(response_json)

            if api_response.code != 200:
                logger.error(f"API Error: {api_response.code} - {api_response.message}")
                raise Exception(f"API Error: {api_response.message}")

            return api_response.data

        except requests.exceptions.RequestException as e:
            logger.error(f"Request Exception: {e}")
            raise
        except Exception as e:
            logger.error(f"General Exception: {e}")
            raise

    def parse_api_response(self, response: Dict) -> Response:
        try:
            api_response = Response(**response)
            return api_response
        except Exception as e:
            logger.error(f"Chyba při parsování odpovědi: {e}")
            raise
