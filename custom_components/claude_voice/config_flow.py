"""Config flow for Claude Voice integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_ANTHROPIC_API_KEY, CONF_ELEVENLABS_API_KEY

class ClaudeVoiceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Claude Voice."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Claude Voice Assistant",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_ANTHROPIC_API_KEY): str,
                vol.Required(CONF_ELEVENLABS_API_KEY): str,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Claude Voice."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_ANTHROPIC_API_KEY, 
                    default=self.config_entry.data.get(CONF_ANTHROPIC_API_KEY)): str,
                vol.Required(CONF_ELEVENLABS_API_KEY,
                    default=self.config_entry.data.get(CONF_ELEVENLABS_API_KEY)): str,
            })
        )
