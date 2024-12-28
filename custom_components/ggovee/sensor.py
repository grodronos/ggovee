from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .GoveeApi.UserDevices.models import Device, Capability
from .const import DOMAIN, MANUFACTURER

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    devices = coordinator.data.get("devices", {})
    for device_id, device in devices.items():
        for capability in device.capabilities:
            match capability.instance:
                case "sensorHumidity":
                    sensors.append(HumiditySensor(coordinator, device_id, capability.instance))
                case "sensorTemperature":
                    sensors.append(TemperatureSensor(coordinator, device_id, capability.instance))
    async_add_entities(sensors, True)

class HumiditySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id, sensor_id):
        super().__init__(coordinator)
        self.device_id = device_id
        self.sensor_id = sensor_id
        self._attr_unique_id = coordinator.data["sensors"][device_id][sensor_id]["unique_id"]
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        coordinator.data["sensors"][device_id][sensor_id]["entity_id"] = seft.entity_id

    @property
    def name(self) -> str:
        return self.coordinator.data["sensors"][self.device_id][self.sensor_id]["name"]

    @property
    def native_value(self) -> float:
        return self.coordinator.data["sensors"][self.device_id][self.sensor_id]["value"]

    @property
    def native_unit_of_measurement(self) -> str:
        return self.coordinator.data["sensors"][self.device_id][self.sensor_id]["unit"]

    @property
    def device_info(self) -> dict:
        device = self.coordinator.data["devices"][self.device_id]
        return {
            "identifiers": {(DOMAIN, self.device_id)},
            "name": device.deviceName,
            "model": device.sku,
            "manufacturer": MANUFACTURER,
        }

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

class TemperatureSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id, sensor_id):
        super().__init__(coordinator)
        self.device_id = device_id
        self.sensor_id = sensor_id
        self._attr_unique_id = coordinator.data["sensors"][device_id][sensor_id]["unique_id"]
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        coordinator.data["sensors"][device_id][sensor_id]["entity_id"] = seft.entity_id

    @property
    def name(self) -> str:
        return self.coordinator.data["sensors"][self.device_id][self.sensor_id]["name"]

    @property
    def native_value(self) -> float:
        return self.coordinator.data["sensors"][self.device_id][self.sensor_id]["value"]

    @property
    def native_unit_of_measurement(self) -> str:
        return self.coordinator.data["sensors"][self.device_id][self.sensor_id]["unit"]

    @property
    def device_info(self) -> dict:
        device = self.coordinator.data["devices"][self.device_id]
        return {
            "identifiers": {(DOMAIN, self.device_id)},
            "name": device.deviceName,
            "model": device.sku,
            "manufacturer": MANUFACTURER,
        }

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success