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
