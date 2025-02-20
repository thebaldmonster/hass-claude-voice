"""Config flow for Claude Voice integration."""
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_ANTHROPIC_API_KEY,
    CONF_ELEVENLABS_API_KEY,
)

class ClaudeVoiceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Claude Voice."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Claude Voice Assistant",
                data={
                    CONF_ANTHROPIC_API_KEY: user_input[CONF_ANTHROPIC_API_KEY],
                    CONF_ELEVENLABS_API_KEY: user_input[CONF_ELEVENLABS_API_KEY],
                }
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ANTHROPIC_API_KEY): str,
                vol.Required(CONF_ELEVENLABS_API_KEY): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
