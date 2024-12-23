from homeassistant import config_entries
import voluptuous as vol
from homeassistant.core import callback
from .const import DOMAIN
from homeassistant.const import (
    CONF_API_KEY,
    CONF_DEVICES,
    CONF_PARAMS,
    CONF_SCAN_INTERVAL,
)

class GgoveeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            api_key = user_input.get(CONF_API_KEY)
            if not api_key:
                errors["base"] = "invalid_api_key"
            else:
                # Zde můžete přidat další validaci API klíče, například ověření u API Govee
                return self.async_create_entry(title="Ggovee", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
