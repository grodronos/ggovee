"""Constants for the Govee integration."""
import logging
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

# Definice loggeru pro použití v dalších souborech (např. sensor.py)
LOGGER = logging.getLogger(__package__)

# Využívané platformy (prozatím jen senzor)
PLATFORMS = [Platform.SENSOR]
