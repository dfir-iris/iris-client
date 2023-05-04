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

    def unmerge_alert(self, alert_id: int, target_case_id: int) -> ApiResponse:
        """ Unmerge an alert

        Args:
            alert_id (int): Alert id
            target_case_id (int): Target case id

        Returns:
            ApiResponse: Response object
        """
        payload = {
            "target_case_id": target_case_id
        }

        return self._s.pi_post(f"alerts/unmerge/{alert_id}", data=payload)

    def filter_alerts(self, alert_title: str = None, alert_description: str = None, alert_source: str = None,
                      alert_tags: str = None, alert_status_id: int = None, alert_severity_id: int = None,
                      alert_classification_id: int = None, alert_customer_id: int = None, alert_start_date: str = None,
                      alert_end_date: str = None, alert_assets: str = None, alert_iocs: str = None, alert_ids: str = None,
                      case_id: int = None, alert_owner_id: int = None,
                      page: int = 1, per_page: int = 20, sort: str = 'desc') -> ApiResponse:
        """ Filter alerts

        Args:
            alert_title (str): Alert title
            alert_description (str): Alert description
            alert_source (str): Alert source
            alert_tags (str): Alert tags
            alert_status_id (int): Alert status id
            alert_severity_id (int): Alert severity id
            alert_classification_id (int): Alert classification id
            alert_customer_id (int): Alert customer id
            alert_start_date (str): Alert start date
            alert_end_date (str): Alert end date
            alert_assets (str): Alert assets
            alert_iocs (str): Alert IOCs
            alert_ids (str): Alert ids
            case_id (int): Case id
            alert_owner_id (int): Alert owner id
            page (int): Page number
            per_page (int): Number of alerts per page
            sort (str): Sort order


        Returns:
            ApiResponse: Response object
        """
        uri = f"alerts/filter?page={page}&per_page={per_page}&sort={sort}"
        if alert_title:
            uri += f"&alert_title={alert_title}"

        if alert_description:
            uri += f"&alert_description={alert_description}"

        if alert_source:
            uri += f"&alert_source={alert_source}"

        if alert_tags:
            uri += f"&alert_tags={alert_tags}"

        if alert_status_id:
            uri += f"&alert_status_id={alert_status_id}"

        if alert_severity_id:
            uri += f"&alert_severity_id={alert_severity_id}"

        if alert_classification_id:
            uri += f"&alert_classification_id={alert_classification_id}"

        if alert_customer_id:
            uri += f"&alert_customer_id={alert_customer_id}"

        if alert_start_date:
            uri += f"&alert_start_date={alert_start_date}"

        if alert_end_date:
            uri += f"&alert_end_date={alert_end_date}"

        if alert_assets:
            uri += f"&alert_assets={alert_assets}"

        if alert_iocs:
            uri += f"&alert_iocs={alert_iocs}"

        if alert_ids:
            uri += f"&alert_ids={alert_ids}"

        if case_id:
            uri += f"&case_id={case_id}"

        if alert_owner_id:
            uri += f"&alert_owner_id={alert_owner_id}"

        return self._s.pi_get(uri)
