from homeassistant import exceptions
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import (
    CRUNCH_JSON_ALL_CLUBS_URL,
    CRUNCH_JSON_CLUB_URL_TEMPLATE,
    CRUNCH_JSON_STATUS,
    CRUNCH_JSON_STATUS_NOT_FOUND,
    CRUNCH_JSON_ID,
    CRUNCH_JSON_NAME,
    CRUNCH_JSON_ADDRESS,
    CRUNCH_JSON_STATE,
    CRUNCH_JSON_CITY,
    CRUNCH_JSON_CURRENT_OCCUPANCY,
    CRUNCH_JSON_MAX_OCCUPANCY,
)


async def _url_to_json(url, session):
    response = await session.get(url)
    return await response.json()


async def list_all_clubs(hass):
    json = await _url_to_json(CRUNCH_JSON_ALL_CLUBS_URL, async_create_clientsession(hass))
    return map(lambda club_json: StaticClub(club_json), json)


class Club:
    def __init__(self, club_id):
        self._club_id = club_id

    @property
    def json(self):
        raise NotImplementedError()

    @property
    def club_id(self):
        return self._club_id

    @property
    def name(self):
        return self.json[CRUNCH_JSON_NAME]

    @property
    def full_name(self):
        club_address = self.json[CRUNCH_JSON_ADDRESS]
        club_state = club_address[CRUNCH_JSON_STATE]
        club_city = club_address[CRUNCH_JSON_CITY]
        return f"{club_state} - {club_city} - {self.name}"

    @property
    def current_occupancy(self):
        return self.json[CRUNCH_JSON_CURRENT_OCCUPANCY]

    @property
    def max_occupancy(self):
        return self.json[CRUNCH_JSON_MAX_OCCUPANCY]


class DynamicClub(Club):
    def __init__(self, club_id, hass):
        super().__init__(club_id)
        self._api_url = CRUNCH_JSON_CLUB_URL_TEMPLATE.format(club_id=club_id)
        self._hass = hass
        self._latest_json = None
        self._successful = True
        self._client_session = async_create_clientsession(self._hass)

    @property
    def json(self):
        return self._latest_json

    async def update(self):
        self._latest_json = await _url_to_json(self._api_url, self._client_session)
        if (
            CRUNCH_JSON_STATUS in self._latest_json
            and self._latest_json[CRUNCH_JSON_STATUS] == CRUNCH_JSON_STATUS_NOT_FOUND
        ):
            raise ClubNotFoundError()
        self._successful = True

    @property
    def successful(self):
        return self._successful


class StaticClub(Club):
    def __init__(self, club_json):
        super().__init__(club_json[CRUNCH_JSON_ID])
        self._json = club_json

    @property
    def json(self):
        return self._json


class ClubNotFoundError(exceptions.HomeAssistantError):
    pass
