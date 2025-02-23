"""Pipeline for Claude Voice Assistant."""
import logging
from typing import Any
import asyncio

from anthropic import AsyncAnthropic
import elevenlabs
from homeassistant.components import assist_pipeline
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    CONF_ANTHROPIC_API_KEY,
    CONF_ELEVENLABS_API_KEY,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_pipeline(hass: HomeAssistant, config_entry) -> None:
    """Set up Claude pipeline."""
    try:
        _LOGGER.debug("Starting Claude Voice pipeline setup")
        
        config = hass.data[DOMAIN][config_entry.entry_id]
        _LOGGER.debug("Got config data")

        # Initialize Anthropic client in executor
        anthropic = await hass.async_add_executor_job(
            lambda: AsyncAnthropic(api_key=config[CONF_ANTHROPIC_API_KEY])
        )
        
        # Initialize ElevenLabs in executor
        await hass.async_add_executor_job(
            lambda: setattr(elevenlabs, 'api_key', config[CONF_ELEVENLABS_API_KEY])
        )

        _LOGGER.debug("Clients initialized")

        async def claude_process(text: str) -> assist_pipeline.PipelineEvent:
            """Process text through Claude."""
            try:
                message = await anthropic.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1024,
                    system="You are a helpful home assistant that can control smart home devices and answer questions knowledgeably.",
                    messages=[{"role": "user", "content": text}]
                )

                return assist_pipeline.PipelineEvent(
                    type="intent-end",
                    data={"text": message.content},
                )

            except Exception as err:
                _LOGGER.error("Error processing Claude request: %s", err)
                return assist_pipeline.PipelineEvent(
                    type="error",
                    data={"error": str(err)},
                )

        # Store the processor
        hass.data[DOMAIN]["processor"] = claude_process
        _LOGGER.debug("Pipeline setup complete")

    except Exception as err:
        _LOGGER.error("Failed to set up Claude Voice pipeline: %s", err)
        raise
