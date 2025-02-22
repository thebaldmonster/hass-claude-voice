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

        def init_clients():
            _LOGGER.debug("Initializing clients")
            anthropic_client = AsyncAnthropic(api_key=config[CONF_ANTHROPIC_API_KEY])
            elevenlabs.api_key = config[CONF_ELEVENLABS_API_KEY]
            return anthropic_client

        # Initialize clients in executor
        anthropic = await hass.async_add_executor_job(init_clients)
        _LOGGER.debug("Clients initialized")

        async def claude_pipeline(pipeline: assist_pipeline.Pipeline, audio_data: bytes | None = None) -> None:
            """Process pipeline from audio data."""
            try:
                message = await anthropic.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1024,
                    system="You are a helpful home assistant that can control smart home devices and answer questions knowledgeably.",
                    messages=[{"role": "user", "content": "How can I help you?"}]
                )

                # Create pipeline event
                event = assist_pipeline.PipelineEvent(
                    type="intent-end",
                    data={"text": message.content},
                )

                pipeline.async_pipeline_event(event)

            except Exception as err:
                _LOGGER.error("Error processing voice command: %s", err)
                event = assist_pipeline.PipelineEvent(
                    type="error",
                    data={"error": str(err)},
                )
                pipeline.async_pipeline_event(event)

        # Register with pipeline
        assist_pipeline.async_pipeline_from_audio(hass, claude_pipeline)
        _LOGGER.debug("Pipeline registered successfully")

    except Exception as err:
        _LOGGER.error("Failed to set up Claude Voice pipeline: %s", err)
        raise
