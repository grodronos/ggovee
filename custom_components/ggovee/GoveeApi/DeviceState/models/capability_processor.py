# GoveeApi/DeviceState/models/capability_processor.py
class CapabilityProcessor:
    def process(self, capability_instance: str, state_value):
        match capability_instance:
            case "sensorHumidity":
                return float(state_value)
            case "sensorTemperature":
                return self.fahrenheit_to_celsius(float(state_value))
            case _:
                return state_value  # Defaultní zpracování pro neznámé instance
    
    def fahrenheit_to_celsius(self, fahrenheit: float) -> float:
        celsius = (fahrenheit - 32.0) * 5.0 / 9.0
        return round(celsius, 3)