from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .GoveeApi.UserDevices.models import Device, Capability
from .const import DOMAIN, MANUFACTURER

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    devices = coordinator.data.get("devices")
    for deviceId, device in devices.items():
        for capability in device.capabilities:
            sensors.append(Sensor(coordinator, deviceId, capability.instance))
    async_add_entities(sensors, True)

class Sensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator, device_id, sensor_id):
        super().__init__(coordinator)
        self.device_id = device_id
        self.sensor_id = sensor_id
        self._attr_unique_id = self.coordinator.data["sensors"][device_id][sensor_id]["unique_id"]
        self._attr_name = self.coordinator.data["sensors"][device_id][sensor_id]["entity_id"]

    @property
    def name(self):
        return self.coordinator.data["sensors"][self.device_id][self.sensor_id]["name"]

    @property
    def state(self):
        return self.coordinator.data["sensors"][self.device_id][self.sensor_id]["value"]

    @property
    def unit_of_measurement(self):
        return self.coordinator.data["sensors"][self.device_id][self.sensor_id]["unit"]

    @property
    def device_info(self):
        device = self.coordinator.data["devices"][self.device_id]
        device_info = {
            "identifiers": {(DOMAIN, self.device_id)},
            "name": device.deviceName,
            "model": device.sku,
            "manufacturer": MANUFACTURER,
        }
        return device_info