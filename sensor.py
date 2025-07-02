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

        if device.get("type") == "doorProtect":
            sensors.append(AjaxOpenCloseSensor(device))

    for hub in ajax.hubs:
        sensors.append(AjaxHubStatusSensor(hub))

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

class AjaxOpenCloseSensor(Entity):
    def __init__(self, device):
        self._device = device
        self._attr_name = f"{device['name']} Deurstatus"
        self._attr_unique_id = f"{device['id']}_open_close"

    @property
    def state(self):
        return "open" if self._device.get("isOpened") else "closed"

    @property
    def device_class(self):
        return "opening"

class AjaxHubStatusSensor(Entity):
    def __init__(self, hub):
        self._hub = hub
        self._attr_name = f"{hub['name']} Alarmstatus"
        self._attr_unique_id = f"{hub['id']}_alarm_status"

    @property
    def state(self):
        return self._hub.get("securityStatus")

    @property
    def icon(self):
        status = self.state
        if status == "armed":
            return "mdi:shield-lock"
        elif status == "disarmed":
            return "mdi:shield-off"
        elif status == "partial":
            return "mdi:shield-half-full"
        return "mdi:shield-alert"
