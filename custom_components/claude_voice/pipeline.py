"""Pipeline for Claude Voice Assistant."""
import logging
from typing import Any

from anthropic import AsyncAnthropic
import elevenlabs
from homeassistant.components import conversation
from homeassistant.components.assist_pipeline import (
    PipelineEvent,
    PipelineEventType,
    PipelineNotFound,
    async_get_pipeline,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import intent

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
        
        # Initialize clients in executor
        anthropic = AsyncAnthropic(api_key=config[CONF_ANTHROPIC_API_KEY])
        elevenlabs.api_key = config[CONF_ELEVENLABS_API_KEY]

        async def process_speech(text: str) -> PipelineEvent:
            """Process speech through Claude."""
            try:
                message = await anthropic.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1024,
                    system="You are a helpful home assistant that can control smart home devices and answer questions knowledgeably.",
                    messages=[{"role": "user", "content": text}]
                )

                response = message.content
                _LOGGER.debug("Claude response: %s", response)

                # Generate speech from response
                audio = elevenlabs.generate(
                    text=response,
                    voice="Josh",
                    model="eleven_multilingual_v2"
                )

                return PipelineEvent(
                    type=PipelineEventType.TTS_END,
                    data={
                        "text": response,
                        "audio": audio,
                    }
                )

            except Exception as err:
                _LOGGER.error("Error processing request: %s", err)
                return PipelineEvent(
                    type=PipelineEventType.ERROR,
                    data={"error": str(err)}
                )

        # Register pipeline handler
        @callback
        def async_pipeline_handler(
            pipeline_id: str,
            event: PipelineEvent,
            service_handler: Any
        ) -> None:
            """Handle pipeline events."""
            if event.type == PipelineEventType.STT_END:
                text = event.data["text"]
                _LOGGER.debug("Processing text: %s", text)
                hass.async_create_task(process_speech(text))

        # Register with conversation agent
        conversation.async_set_agent(
            hass,
            config_entry,
            process_speech
        )

        _LOGGER.debug("Pipeline setup complete")

    except Exception as err:
        _LOGGER.error("Failed to set up Claude Voice pipeline: %s", err)
        raise
