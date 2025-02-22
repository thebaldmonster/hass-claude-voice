"""Support for Claude conversations."""
import logging
from typing import Any

from anthropic import Anthropic
from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import TemplateVarsType

from .const import CONF_ANTHROPIC_API_KEY, DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Set up Claude conversation."""
    anthropic = Anthropic(api_key=entry.data[CONF_ANTHROPIC_API_KEY])

    async def async_process(
        text: str, conversation_id: str | None = None, context: TemplateVarsType = None
    ) -> conversation.ConversationResult:
        """Process a sentence."""
        try:
            response = await anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                system="You are a helpful home assistant that can control smart home devices and answer questions knowledgeably. Keep responses concise for voice.",
                messages=[{"role": "user", "content": text}]
            )

            return conversation.ConversationResult(
                response.content,
                confidence=1.0,
            )
        except Exception as err:
            _LOGGER.error("Error processing Claude request: %s", err)
            return conversation.ConversationResult(
                "I'm sorry, I encountered an error processing your request.",
                confidence=1.0,
            )

    conversation.async_set_agent(hass, entry, async_process)
    return True
