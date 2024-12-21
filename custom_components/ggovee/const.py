"""Constants for the Govee integration."""
from homeassistant.const import TEMP_CELSIUS, Platform

DOMAIN = "ggovee"
CONF_API_KEY = "api_key"
CONF_SERVER_REGION = "server_region"
DEFAULT_SERVER_REGION = "us"
SUPPORTED_REGIONS = ["us", "eu"]

STORAGE_KEY = "ggovee_data"
STORAGE_VERSION = 1

MANUFACTURER = "Govee"
BRAND = "Govee"

UPDATE_INTERVAL = 300

# Tady doplňujeme PLATFORMS,
# podle toho, jaké platformy váš kód používá.
# V repozitáři vidím pouze `sensor.py`, takže:
PLATFORMS = [Platform.SENSOR]
