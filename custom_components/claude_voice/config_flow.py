"""Config flow for Claude Voice Assistant."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_ANTHROPIC_API_KEY, CONF_ELEVENLABS_API_KEY

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ANTHROPIC_API_KEY): str,
        vol.Required(CONF_ELEVENLABS_API_KEY): str,
    }
)

class ClaudeVoiceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Claude Voice Assistant."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                # Validate the data can be used to set up the integration
                # but actually do the setup in async_setup_entry
                return self.async_create_entry(
                    title="Claude Voice Assistant",
                    data=user_input,
                )
            except Exception:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
