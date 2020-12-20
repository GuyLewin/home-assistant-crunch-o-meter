import voluptuous as vol
from collections import OrderedDict
import logging

from homeassistant import config_entries

from .const import DOMAIN, CONF_CLUB
from .club import list_all_clubs, ClubNotFoundError


_LOGGER = logging.getLogger(__name__)


class CrunchOMeterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    def __init__(self):
        self._clubs = {}

    async def _create_club_name_list(self):
        club_names_unsorted = {}
        clubs = await list_all_clubs(self.hass)
        for club in clubs:
            club_names_unsorted[club.club_id] = club.full_name
        club_names_sorted_items = sorted(
            club_names_unsorted.items(), key=lambda key_value: key_value[1]
        )
        return OrderedDict(club_names_sorted_items)

    async def async_step_user(self, user_input):
        errors = {}
        if len(self._clubs) == 0:
            self._clubs = await self._create_club_name_list()

        if user_input is not None:
            try:
                club = self._clubs[user_input[CONF_CLUB]]
                return self.async_create_entry(title=club, data=user_input)
            except ClubNotFoundError:
                errors["base"] = "invalid_club_id"
            except Exception as e:
                _LOGGER.exception(e)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_CLUB): vol.In(self._clubs)}),
            errors=errors,
        )
