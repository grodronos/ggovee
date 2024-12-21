from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class TvojeIntegraceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            api_key = user_input.get("api_key")
            if not api_key:
                errors["base"] = "invalid_api_key"
            else:
                return self.async_create_entry(title="ggovee", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("api_key"): str,
            }),
            errors=errors,
        )
