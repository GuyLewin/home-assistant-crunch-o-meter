from homeassistant.helpers.entity import Entity

from .const import (
    CONF_CLUB,
    UNIT_OF_MEASUREMENT,
    CURRENT_OCCUPANCY_SENSOR_ID,
    CURRENT_OCCUPANCY_SENSOR_NAME,
    MAX_OCCUPANCY_SENSOR_ID,
    MAX_OCCUPANCY_SENSOR_NAME,
)
from .club import DynamicClub


async def async_setup_entry(hass, entry, async_add_devices):
    club_id = entry.data[CONF_CLUB]
    club = DynamicClub(club_id, hass)
    await club.update()

    new_devices = []
    new_devices.append(CurrentOccupancy(club))
    new_devices.append(MaxOccupancy(club))

    async_add_devices(new_devices)


class SensorBase(Entity):
    should_poll = True
    SENSOR_ID = "N/A"
    SENSOR_NAME = "N/A"

    def __init__(self, club, should_update):
        self._club = club
        self._should_update = should_update
        self._state = None

    @property
    def unique_id(self):
        return f"{self._club.club_id}_{self.__class__.SENSOR_ID}"

    @property
    def name(self):
        return f"Crunch {self._club.name} {self.__class__.SENSOR_NAME}"

    @property
    def available(self):
        return self._club.successful

    @property
    def unit_of_measurement(self):
        return UNIT_OF_MEASUREMENT

    async def async_update(self):
        if not self._should_update:
            return
        await self._club.update()


class CurrentOccupancy(SensorBase):
    SENSOR_ID = CURRENT_OCCUPANCY_SENSOR_ID
    SENSOR_NAME = CURRENT_OCCUPANCY_SENSOR_NAME

    def __init__(self, club):
        super().__init__(club, True)

    @property
    def state(self):
        return self._club.current_occupancy


class MaxOccupancy(SensorBase):
    SENSOR_ID = MAX_OCCUPANCY_SENSOR_ID
    SENSOR_NAME = MAX_OCCUPANCY_SENSOR_NAME

    def __init__(self, club):
        # Only 1 sensor should keep the club updated
        # Not updating here means this sensor will always be 1 SCAN_INTERVAL behind
        # (since the update is async, this update will return fast )
        # but this value rarely changes, so this is acceptable
        super().__init__(club, False)

    @property
    def state(self):
        return self._club.max_occupancy
