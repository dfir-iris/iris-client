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
import json
import warnings
from typing import List

from requests import Response

from dfir_iris_client.helper.utils import ApiResponse, ClientApiError
from dfir_iris_client.session import ClientSession


class Alert(object):
    """Handles alert operations"""

    def __init__(self, session: ClientSession):
        """Init

        Args:
            session (ClientSession): Client session
        """
        self._s = session

    def get_alert(self, alert_id: int) -> ApiResponse:
        """Get an alert

        Args:
            alert_id (int): Alert id

        Returns:
            Response: Response object
        """
        return self._s.pi_get(f"/alerts/{alert_id}")

    def get_alerts(self, alert_ids: List[int]) -> ApiResponse:
        """Get alerts from their ids

        Args:
            alert_ids (list): Alert ids

        Returns:
            Response: Response object
        """

        if not all(isinstance(element, int) for element in alert_ids):
            return ClientApiError('Expected a list of integers for alert_ids')

        return self._s.pi_get(f"/alerts/filter?alert_ids={','.join(str(element) for element in alert_ids)}")


