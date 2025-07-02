### custom_components/ajax_manager/__init__.py
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

from python_ajax_manager import AjaxManager

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    ajax = AjaxManager(username=entry.data["username"], password=entry.data["password"])
    await hass.async_add_executor_job(ajax.login)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = ajax

    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True


### custom_components/ajax_manager/manifest.json
{
  "domain": "ajax_manager",
  "name": "AJAX Alarm Manager",
  "version": "0.1.0",
  "requirements": [
    "git+https://github.com/Den901/python_ajax_manager.git"
  ],
  "codeowners": ["@yourgithub"],
  "config_flow": false,
  "documentation": "https://github.com/Den901/python_ajax_manager"
}


### custom_components/ajax_manager/const.py
DOMAIN = "ajax_manager"


### custom_components/ajax_manager/sensor.py
import logging
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    ajax = hass.data[DOMAIN][config_entry.entry_id]
    await ajax.fetch_objects()

    sensors = []
    for device in ajax.devices:
        sensors.append(AjaxBatterySensor(device))

    async_add_entities(sensors)

class AjaxBatterySensor(Entity):
    def __init__(self, device):
        self._device = device
        self._attr_name = f"{device['name']} Battery"
        self._attr_unique_id = f"{device['id']}_battery"

    @property
    def state(self):
        return self._device.get("batteryLevel")

    @property
    def device_class(self):
        return "battery"

    @property
    def unit_of_measurement(self):
        return "%"
