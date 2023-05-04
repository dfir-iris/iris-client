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
            ApiResponse: Response object
        """
        return self._s.pi_get(f"alerts/{alert_id}")

    def get_alerts(self, alert_ids: List[int]) -> ApiResponse:
        """Get alerts from their ids

        Args:
            alert_ids (list): Alert ids

        Returns:
            ApiResponse: Response object
        """

        if not all(isinstance(element, int) for element in alert_ids):
            return ClientApiError('Expected a list of integers for alert_ids')

        return self._s.pi_get(f"alerts/filter?alert_ids={','.join(str(element) for element in alert_ids)}")

    def add_alert(self, alert_data: dict) -> ApiResponse:
        """Add an alert

        Args:
            alert_data (dict): Alert data - The data is defined in the API documentation

        Returns:
            ApiResponse: Response object
        """
        return self._s.pi_post("alerts/add", alert_data)

    def update_alert(self, alert_id: int, alert_data: dict) -> ApiResponse:
        """Update an alert

        Args:
            alert_id (int): Alert id
            alert_data (dict): Alert data - The data is defined in the API documentation

        Returns:
            ApiResponse: Response object
        """
        return self._s.pi_post(f"alerts/update/{alert_id}", alert_data)

    def delete_alert(self, alert_id: int) -> ApiResponse:
        """Delete an alert

        Args:
            alert_id (int): Alert id

        Returns:
            ApiResponse: Response object
        """
        return self._s.pi_post(f"alerts/delete/{alert_id}")

    def escalate_alert(self, alert_id: int, iocs_import_list: List[str], assets_import_list: List[str],
                       escalation_note: str, case_title:str, case_tags: str, case_template_id: int = None,
                       import_as_event: bool = False) -> ApiResponse:
        """Escalate an alert

        Args:
            alert_id (int): Alert id
            iocs_import_list (list): List of IOCs UUID from the alert to import
            assets_import_list (list): List of assets UUIDs from the alert to import
            escalation_note (str): Escalation note
            case_title (str): Case title
            case_tags (str): Case tags, a string of comma separated tags
            case_template_id (int): Case template id
            import_as_event (bool): Import as event

        Returns:
            ApiResponse: Response object
        """
        payload = {
            "iocs_import_list": iocs_import_list,
            "assets_import_list": assets_import_list,
            "note": escalation_note,
            "case_title": case_title,
            "case_tags": case_tags,
            "case_template_id": case_template_id,
            "import_as_event": import_as_event
        }

        return self._s.pi_post(f"alerts/escalate/{alert_id}", data=payload)

    def merge_alert(self, alert_id: int, target_case_id: int, iocs_import_list: List[str],
                    assets_import_list: List[str], merge_note: str, import_as_event: bool = False) -> ApiResponse:
        """Merge an alert

        Args:
            alert_id (int): Alert id
            target_case_id (int): Target case id
            iocs_import_list (list): List of IOCs UUID from the alert to import
            assets_import_list (list): List of assets UUIDs from the alert to import
            merge_note (str): Merge note
            import_as_event (bool): Import as event

        Returns:
            ApiResponse: Response object
        """
        payload = {
            "target_case_id": target_case_id,
            "iocs_import_list": iocs_import_list,
            "assets_import_list": assets_import_list,
            "note": merge_note,
            "import_as_event": import_as_event
        }

        return self._s.pi_post(f"alerts/merge/{alert_id}", data=payload)

