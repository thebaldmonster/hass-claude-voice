"""Conversation component for Claude Voice."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Claude Voice conversation."""
    agent = ClaudeConversationAgent(hass, entry)
    conversation.async_set_agent(hass, entry, agent)
    return True

class ClaudeConversationAgent(conversation.AbstractConversationAgent):
    """Claude Conversation Agent."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.target_agent = conversation.DEFAULT_AGENT

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return ["en"]

    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        """Process a sentence."""
        response = await self.hass.components.conversation.async_converse(
            user_input.text,
            user_input.conversation_id,
            user_input.context,
            self.target_agent,
        )
        return response

    @property
    def attribution(self) -> str:
        """Return the attribution."""
        return "Powered by Claude"
