"""Pipeline for Claude Voice Assistant."""
import logging
from typing import Any
import asyncio

from anthropic import AsyncAnthropic
from homeassistant.components import conversation
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import singleton

from .const import (
    DOMAIN,
    CONF_ANTHROPIC_API_KEY,
    CONF_ELEVENLABS_API_KEY,
)

_LOGGER = logging.getLogger(__name__)

@singleton.singleton("claude_voice_client")
async def get_anthropic_client(hass: HomeAssistant, api_key: str):
    """Get Anthropic client."""
    async def init_client():
        return AsyncAnthropic(api_key=api_key)
    return await hass.async_add_executor_job(lambda: AsyncAnthropic(api_key=api_key))

async def process_with_claude(hass: HomeAssistant, text: str, api_key: str) -> str:
    """Process text with Claude."""
    client = await get_anthropic_client(hass, api_key)
    response = await client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        system="You are a helpful home assistant that can control smart home devices and answer questions knowledgeably.",
        messages=[{"role": "user", "content": text}]
    )
    return response.content
