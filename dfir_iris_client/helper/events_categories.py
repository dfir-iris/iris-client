#  IRIS Client API Source Code
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
from typing import Union

from dfir_iris_client.helper.utils import ApiResponse


class EventCategoryHelper(object):
    """Handles the event category methods"""
    def __init__(self, session):
        self._s = session

    def list_events_categories(self) -> ApiResponse:
        """Returns a list of all events categories available

        Args:

        Returns:
            ApiResponse object
        """
        return self._s.pi_get('manage/event-categories/list')

    def lookup_event_category_name(self, event_category: str) -> Union[None, int]:
        """Returns an event category ID from its name otherwise None

        Args:
          event_category: Name of the event to lookup

        Returns:
          Union[None, int]: Event category ID matching provided event_category name

        """
        evt_list = self.list_events_categories()
        if evt_list:
            for evt in evt_list.get_data():
                if evt.get('name').lower() == event_category.lower():
                    return evt.get('id')

        return None

    def get_event_category(self, event_category_id: int) -> ApiResponse:
        """Returns an event category from its ID

        Args:
          event_category_id: Event category to lookup

        Returns:
          ApiResponse object

        """
        return self._s.pi_get(f'manage/event-categories/{event_category_id}')