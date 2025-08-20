# GoveeApi/DeviceState/models/capability_processor.py
class CapabilityProcessor:
    def process(self, capability_instance: str, state_value):
        match capability_instance:
            case "sensorHumidity":
                v = state_value.get("value") if isinstance(state_value, dict) else state_value
                return float(v) if v not in ("", None) else 0.0
            case "sensorTemperature":
                v = state_value.get("value") if isinstance(state_value, dict) else state_value
                return self.fahrenheit_to_celsius(float(v)) if v not in ("", None) else 0.0
            case "online":
                v = state_value.get("value") if isinstance(state_value, dict) else state_value
                return bool(v) if v not in ("", None) else False
            case _:
                return state_value  # Defaultní zpracování pro neznámé instance

    def fahrenheit_to_celsius(self, fahrenheit: float) -> float:
        celsius = (fahrenheit - 32.0) * 5.0 / 9.0
        return round(celsius, 3)