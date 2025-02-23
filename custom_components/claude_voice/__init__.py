"""The Claude Voice integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components import conversation
from homeassistant.components.assist_pipeline import (
    PipelineNotFound,
    async_create_default_pipeline,
)

from .const import DOMAIN
from .pipeline import async_setup_pipeline

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["conversation"]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Claude Voice component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Claude Voice from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await async_setup_pipeline(hass, entry)

    # Create default pipeline if none exists
    try:
        await async_create_default_pipeline(
            hass,
            name="Claude Voice Assistant",
            conversation_engine="claude_voice",
            language="en"
        )
    except Exception as err:
        _LOGGER.error("Failed to create default pipeline: %s", err)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
