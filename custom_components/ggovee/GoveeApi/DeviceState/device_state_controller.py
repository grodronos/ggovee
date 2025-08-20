# GoveeApi/UserDevices/controller.py
# Response JSON: {'requestId': 'e454bd7a-4098-4fc0-97de-edbe77bb50b0', 'msg': 'success', 'code': 200, 'payload': {
# 'sku': 'H5179', 
# 'device': '59:7C:1F:64:04:40:EC:83', 
# 'capabilities': [
#     {
#         'type': 'devices.capabilities.online', 
#         'instance': 'online', 
#         'state': {'value': True}
#     }, 
#     {
#         'type': 'devices.capabilities.property',
#         'instance': 'sensorTemperature',
#         'state': {'value': 55.76}
#     }, 
#     {
#         'type': 'devices.capabilities.property',
#         'instance': 'sensorHumidity', 
#         'state': {'value': 73.1}
#     }
# ]}}

import requests
from typing import List, Dict
from .models import Response, Payload, Capability
import logging
import uuid
import json

logger = logging.getLogger(__name__)

class DeviceStateController:
    def __init__(self, api_key: str, timeout: int = 10):
        self.base_url = "https://openapi.api.govee.com/router/api/v1"
        self.timeout = timeout
        self.headers={
            "Content-Type":"application/json",
            "Govee-API-Key": api_key
        }
        path = 'device/state'
        self.url = f"{self.base_url}/{path.strip('/')}"

    async def getDeviceState(self, hass, device) -> Payload:
        data = '{"requestId": "'+ str(uuid.uuid4()) + '","payload": {"sku": "' + device.sku + '","device": "' + device.device + '"}}'
        data = json.loads(data)

        try:
            response = await hass.async_add_executor_job(lambda: requests.post(self.url,json=data,headers=self.headers,timeout=self.timeout))
            if response.status_code != 200:
                logger.error(f"HTTP Error: {response.status_code} - {response.text}")
                response.raise_for_status()

            response_json = json.loads(response.text)
            api_response = self.parse_api_response(response_json)

            if api_response.code != 200:
                logger.error(f"API Error: {api_response.code} - {api_response.message}")
                raise Exception(f"API Error: {api_response.message}")

            return api_response.payload.capabilities

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
