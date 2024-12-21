"""Constants for the Govee integration."""
from datetime import timedelta
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

# Nastavíme interval updatů na 5 minut (300 sekund)
UPDATE_INTERVAL = timedelta(seconds=300)

# Pokud používáte pouze sensor platformu, stačí:
PLATFORMS = [Platform.SENSOR]
