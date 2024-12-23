"""Constants for the Govee integration."""
import logging
from datetime import timedelta
from homeassistant.const import TEMP_CELSIUS, Platform

DOMAIN = "ggovee"

MANUFACTURER = "Govee"

# Nastavíme interval updatů na 5 minut (300 sekund)
UPDATE_INTERVAL = timedelta(seconds=300)