"""Crunch-O-Meter integration."""

from .const import DOMAIN, VERSION, ISSUE_URL, PLATFORM
import logging


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config_entry):
    """ Disallow configuration via YAML """
    return True


async def async_setup_entry(hass, config_entry):
    """Load the saved entities."""
    _LOGGER.info(
        "Version %s is starting, if you have any issues please report" " them here: %s",
        VERSION,
        ISSUE_URL,
    )
    hass.config_entries.async_update_entry = config_entry.data
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, PLATFORM)
    )
    return True


async def async_unload_entry(hass, config_entry):
    """Handle removal of an entry."""
    try:
        await hass.config_entries.async_forward_entry_unload(config_entry, PLATFORM)
        _LOGGER.info("Successfully removed sensor from the " + DOMAIN + " integration")
    except ValueError:
        pass
    return True
