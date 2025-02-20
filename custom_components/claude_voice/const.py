"""Constants for the Claude Voice integration."""
from homeassistant.const import Platform

DOMAIN = "claude_voice"
PLATFORMS = [Platform.ASSIST_PIPELINE]

CONF_ANTHROPIC_API_KEY = "anthropic_api_key"
CONF_ELEVENLABS_API_KEY = "elevenlabs_api_key"
CONF_WAKE_WORDS = "wake_words"
CONF_VOICE_ID = "voice_id"
CONF_PROMPT = "prompt"

DEFAULT_WAKE_WORDS = {
    "yo craig": {
        "prompt": "You are Craig, a friendly and helpful assistant. Respond in a casual, laid-back manner while maintaining access to home automation controls.",
        "voice_id": ""
    },
    "hey professor": {
        "prompt": "You are a knowledgeable professor. Explain concepts clearly and thoroughly while maintaining access to home automation controls.",
        "voice_id": ""
    }
}
