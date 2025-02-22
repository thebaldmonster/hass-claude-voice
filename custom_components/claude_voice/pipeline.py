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

        async def claude_pipeline(text: str) -> assist_pipeline.PipelineEvent:
            """Process text through Claude."""
            try:
                _LOGGER.debug("Processing text: %s", text)
                message = await anthropic.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1024,
                    system="You are a helpful home assistant that can control smart home devices and answer questions knowledgeably.",
                    messages=[{"role": "user", "content": text}]
                )
                _LOGGER.debug("Got response from Claude")

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

        # Register the pipeline
        _LOGGER.debug("Registering pipeline")
        assist_pipeline.async_register_pipeline(
            hass,
            "claude_voice",
            "Claude Voice Assistant",
            "claude_pipeline",
            claude_pipeline,
        )
        _LOGGER.debug("Pipeline registered successfully")

    except Exception as err:
        _LOGGER.error("Failed to set up Claude Voice pipeline: %s", err)
        raise
