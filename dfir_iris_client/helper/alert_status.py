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


class AlertStatusHelper(object):
    """Handles the alert status methods"""

    def __init__(self, session):
        self._s = session

    def list_alert_status_types(self) -> ApiResponse:
        """
        Returns a list of all alert statuses

        Args:

        Returns:
            APIResponse object
        """
        return self._s.pi_get('manage/alert-status/list')

    def lookup_alert_status_name(self, alert_status_name: str) -> Union[int, None]:
        """
        Returns an alert status ID from its name otherwise None

        Args:
          alert_status_name: str:

        Returns:
          Union[int, None] - alert status ID matching provided alert status name or None if not found

        """
        ast_list = self.list_alert_status_types()
        for ast in ast_list.get_data():
            if ast.get('status_name').lower() == alert_status_name.lower():
                return ast.get('status_id')

        return None

    def get_alert_status(self, alert_status_id: int) -> ApiResponse:
        """
        Returns an alert status from its ID

        Args:
          alert_status_id: int:

        Returns:
          APIResponse object

        """
        return self._s.pi_get('manage/alert-status/{}'.format(alert_status_id))