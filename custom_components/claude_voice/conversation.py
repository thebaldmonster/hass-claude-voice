"""Conversation component for Claude Voice."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .pipeline import process_with_claude

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities=None) -> bool:
    """Set up Claude Voice conversation."""
    _LOGGER.debug("Setting up Claude Voice conversation")
    api_key = entry.data["anthropic_api_key"]
    
    conversation_agent = ClaudeConversationAgent(hass, api_key)
    conversation.async_set_agent(hass, entry, conversation_agent)
    
    return True

class ClaudeConversationAgent(conversation.AbstractConversationAgent):
    """Claude Conversation Agent."""

    def __init__(self, hass: HomeAssistant, api_key: str) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.api_key = api_key
        _LOGGER.debug("Initialized Claude Conversation Agent")

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return ["en"]

    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        """Process a sentence."""
        try:
            _LOGGER.debug("Processing conversation input: %s", user_input.text)
            
            response = await process_with_claude(
                self.hass,
                user_input.text,
                self.api_key
            )
            
            _LOGGER.debug("Got Claude response: %s", response)

            return conversation.ConversationResult(
                response=response,
                conversation_id=user_input.conversation_id
            )

        except Exception as err:
            _LOGGER.error("Error in conversation processing: %s", err)
            return conversation.ConversationResult(
                response=f"I encountered an error: {str(err)}",
                conversation_id=user_input.conversation_id
            )
