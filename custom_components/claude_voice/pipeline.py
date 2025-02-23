"""Pipeline for Claude Voice Assistant."""
import logging
from typing import Any
import asyncio

from anthropic import AsyncAnthropic
from homeassistant.core import HomeAssistant
from homeassistant.helpers import singleton

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

@singleton.singleton("claude_voice_client")
async def get_anthropic_client(hass: HomeAssistant, api_key: str):
    """Get Anthropic client."""
    def create_client():
        return AsyncAnthropic(api_key=api_key)
    return await hass.async_add_executor_job(create_client)

async def process_with_claude(hass: HomeAssistant, text: str, api_key: str) -> str:
    """Process text with Claude."""
    try:
        _LOGGER.debug("Getting Claude client")
        client = await get_anthropic_client(hass, api_key)
        
        _LOGGER.debug("Sending request to Claude")
        response = await client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            system="You are a helpful home assistant that can control smart home devices and answer questions knowledgeably. Keep responses concise and natural.",
            messages=[{"role": "user", "content": text}]
        )
        
        _LOGGER.debug("Got response from Claude")
        return response.content
    except Exception as err:
        _LOGGER.error("Error in Claude processing: %s", err)
        raise
