import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

class GoveeH5179ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow pro Govee H5179 integraci."""

    async def async_step_user(self, user_input=None):
        """Zpracování inicializačního kroku."""
        if user_input is not None:
            return self.async_create_entry
::contentReference[oaicite:0]{index=0}