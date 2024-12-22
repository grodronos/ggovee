"""Support for Govee bluetooth sensors."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .GoveeApi.UserDevices.controller import Controller
from .GoveeApi.UserDevices.models import Device
from .const import DOMAIN, STARTUP_MESSAGE
from .coordinator import GoveeDataUpdateCoordinator
from typing import Final
import logging
import asyncio

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Govee from a config entry."""

    _LOGGER.debug("grodronos")
    controller = Controller(api_key=str(entry.data.get(CONF_API_KEY, None)))

    try:
        # Získání zařízení
        devices: List[Device] = await controller.getDevices(hass)
         # Výpis zařízení
        print(f"Získáno zařízení: {len(devices)}")
        for device in devices:
            print(f"Zařízení: {device.deviceName} ({device.device})")
            for capability in device.capabilities:
                print(f"  - {capability.instance}")
    except Exception as e:
        print(f"Chyba: {e}")

    # Vytvoříme instanci koordinátoru:
    coordinator = GoveeDataUpdateCoordinator(hass, entry)

    # Provedeme první (blokující) refresh, aby se natáhla data
    await coordinator.async_config_entry_first_refresh()

    # Zeptáme se koordinátoru na data (koordinátor musí vracet něco jako {"device": {...}, ...})
    device = None
    if coordinator.data:
        device = coordinator.data.get("device")

    # Uložíme data do hass.data - sem si pak "sáhne" platforma sensor.py
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "device": device,  # Ukládáme device, aby byl k dispozici v sensor.py i jinde
    }

    # Dopředné nastavení platformy sensor
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Govee config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
