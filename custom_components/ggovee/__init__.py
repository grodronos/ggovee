"""Support for Govee bluetooth sensors."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, STARTUP_MESSAGE
from .coordinator import GoveeDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Govee from a config entry."""
    _LOGGER.info("__init__:async_setup_entry")

    # Vytvoříme instanci koordinátoru:
    coordinator = GoveeDataUpdateCoordinator(hass, entry)

    # Provedeme první (blokující) refresh, aby se natáhla data
    await coordinator.async_config_entry_first_refresh()

    # Zeptáme se koordinátoru na data (koordinátor musí vracet něco jako {"device": {...}, ...})
    device = None
    if coordinator.data:
        device = coordinator.data.get("device")

    # Uložíme data do hass.data - sem si pak "sáhne" platforma sensor.py nebo climate.py
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "device": device,  # Ukládáme device, aby byl k dispozici v sensor.py i jinde
    }

    # Dopředné nastavení platformy sensor (to samé pro climate)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "climate")
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Govee config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "climate"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
