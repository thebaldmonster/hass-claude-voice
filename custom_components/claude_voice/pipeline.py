"""Pipeline for Claude Voice Assistant."""
import logging
from typing import Any
import asyncio

from anthropic import AsyncAnthropic
from homeassistant.core import HomeAssistant
from homeassistant.helpers import singleton

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

def create_anthropic_client(api_key: str):
    """Create Anthropic client in executor."""
    _LOGGER.debug("Creating new Anthropic client")
    return AsyncAnthropic(api_key=api_key)

async def process_with_claude(hass: HomeAssistant, text: str, api_key: 
str) -> str:
    """Process text with Claude."""
    try:
        _LOGGER.debug("Starting Claude processing with text: %s", text)
        # Create client in executor to avoid blocking calls
        client = await 
hass.async_add_executor_job(create_anthropic_client, api_key)
        
        _LOGGER.debug("Got client, sending request to Claude")
        response = await client.messages.create(
            model="claude-3-sonnet",  # This is the correct model name
            max_tokens=1024,
            system="You are Claude, an AI assistant integrated with Home 
Assistant. You can help with home automation and answer questions. Always 
acknowledge that you are Claude when asked.",
            messages=[{
                "role": "user",
                "content": text
            }]
        )
        
        _LOGGER.debug("Got response from Claude: %s", response.content)
        return response.content

    except Exception as err:
        _LOGGER.error("Error in Claude processing: %s", str(err))
        return f"I encountered an error: {str(err)}"
