"""Assist pipeline for Claude Voice."""
import logging
from typing import Any
from anthropic import Anthropic
import elevenlabs
from homeassistant.components import assist_pipeline
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.assist_pipeline.pipeline import Pipeline, PipelineEvent, PipelineData

from .const import (
    DOMAIN,
    DEFAULT_WAKE_WORDS,
    CONF_ANTHROPIC_API_KEY,
    CONF_ELEVENLABS_API_KEY,
)

_LOGGER = logging.getLogger(__name__)

async def async_pipeline_from_audio(pipeline_data: PipelineData, audio_data: bytes) -> None:
    """Process pipeline from audio data."""
    try:
        # Initialize Anthropic and ElevenLabs clients
        config = pipeline_data.hass.data[DOMAIN][list(pipeline_data.hass.data[DOMAIN].keys())[0]]
        anthropic = Anthropic(api_key=config[CONF_ANTHROPIC_API_KEY])
        elevenlabs.set_api_key(config[CONF_ELEVENLABS_API_KEY])
# Process audio to text (using Home Assistant's STT)
        stt_pipeline = pipeline_data.pipeline.stt_pipeline
        if stt_pipeline:
            text = await stt_pipeline.async_process_audio(audio_data)
        else:
            raise assist_pipeline.PipelineError("No STT pipeline configured")

        # Get response from Claude
        message = await anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            system="You are a helpful home assistant that can control smart home devices and answer questions knowledgeably. Keep responses concise for voice.",
            messages=[{"role": "user", "content": text}]
        )

        response_text = message.content

        # Convert to speech using ElevenLabs
        audio = elevenlabs.generate(
            text=response_text,
            voice="Josh",  # Default voice, can be configured
            model="eleven_multilingual_v2"
        )# Create pipeline event
        event = PipelineEvent(
            type="intent-end",
            data={
                "text": response_text,
                "audio": audio,
            },
        )

        await pipeline_data.async_process_event(event)

    except Exception as err:
        _LOGGER.error("Error processing voice command: %s", err)
        event = PipelineEvent(
            type="error",
            data={"error": str(err)},
        )
        await pipeline_data.async_process_event(event)
