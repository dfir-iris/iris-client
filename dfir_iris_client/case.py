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

from requests import Response

from dfir_iris_client.helper.case_classifications import CaseClassificationsHelper
from dfir_iris_client.session import ClientSession

from dfir_iris_client.customer import Customer
from dfir_iris_client.admin import AdminHelper
from dfir_iris_client.helper.assets_type import AssetTypeHelper
from dfir_iris_client.helper.analysis_status import AnalysisStatusHelper
from dfir_iris_client.helper.compromise_status import CompromiseStatusHelper
from dfir_iris_client.helper.errors import IrisClientException
from dfir_iris_client.helper.ioc_types import IocTypeHelper
from dfir_iris_client.helper.events_categories import EventCategoryHelper
from dfir_iris_client.helper.task_status import TaskStatusHelper
from dfir_iris_client.users import User
from dfir_iris_client.helper.tlps import TlpHelper
from dfir_iris_client.helper.utils import ClientApiError, ApiResponse, get_data_from_resp

from typing import Union, List, BinaryIO
import datetime
import urllib.parse


class Case(object):
    """Handles the case methods"""

    def __init__(self, session: ClientSession, case_id: int = None):
        self._s = session
        self._cid = case_id

    def list_cases(self) -> ApiResponse:
        """
        Returns a list of all the cases
        
        :return: ApiResponse

        Args:

        Returns:

        """
        cid = self._assert_cid(cid=1)
        return self._s.pi_get('manage/cases/list', cid=cid)

    def get_case(self, cid: int) -> ApiResponse:
        """Gets an existing case from its ID

        Args:
          cid: CaseID to fetch

        Returns:
          ApiResponse object

        """
        return self._s.pi_get(f'manage/cases/{cid}')

    def add_case(self, case_name: str, case_description: str, case_customer: Union[str, int],
                 case_classification: Union[str, int],soc_id: str, custom_attributes: dict = None,
                 create_customer=False) -> ApiResponse:
        """Creates a new case. If create_customer is set to true and the customer doesn't exist,
        it is created. Otherwise an error is returned.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          case_name: case_name
          case_classification: Classification of the case
          case_description: Description of the case
          case_customer: Name or ID of the customer
          soc_id: SOC Number
          custom_attributes: Custom attributes of the case
          create_customer: Set to true to create the customer is doesn't exists. (Default value = False)

        Returns:
          ApiResponse object

        """
        if isinstance(case_customer, str):
            # Get the customer ID
            customer = Customer(session=self._s)
            c_id = customer.lookup_customer(customer_name=case_customer)

            if c_id.is_error():
                if create_customer:
                    adm = AdminHelper(self._s)
                    c_resp = adm.add_customer(customer_name=case_customer)
                    if c_resp.is_error():
                        return c_resp

                    c_id = c_resp

                else:

                    return ClientApiError(f'Customer {case_customer} wasn\'t found. Check syntax or set '
                                          f'create_customer flag to create it')

            if c_id.is_error():
                return c_id

            case_customer = c_id.get_data().get('customer_id')

        if isinstance(case_classification, str):
            csh = CaseClassificationsHelper(self._s)
            case_classification = csh.lookup_case_classification_name(case_classification_name=case_classification)
            if case_classification is None:
                return ClientApiError(f'Case classification {case_classification} wasn\'t found. Check syntax.')

        else:
            case_classification = int(case_classification)

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "case_name": case_name,
            "case_customer": case_customer,
            "classification": case_classification,
            "case_soc_id": soc_id,
            "case_description": case_description,
            "custom_attributes": custom_attributes
        }
        resp = self._s.pi_post('manage/cases/add', data=body)

        return resp

    def update_case(self, case_id: int, case_name: str = None, case_description: str = None,
                    soc_id: str = None, case_tags: List[str] = None,
                    custom_attributes: dict = None) -> ApiResponse:
        """Updates an existing case. If create_customer is set to true and the customer doesn't exist,
        it is created. Otherwise an error is returned.

        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        If a value is not provided, it is not updated.

        Args:
          case_id: ID of the case to update
          case_name: case_name
          case_description: Description of the case
          case_tags: List of tags to add to the case
          soc_id: SOC Number
          custom_attributes: Custom attributes of the case

        Returns:
            ApiResponse object

            """

        case = self.get_case(case_id)
        if case.is_error():
            return case

        case_data = get_data_from_resp(case)

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        if custom_attributes is None:
            custom_attributes = case_data.get('custom_attributes')

        if case_description is None:
            case_description = case_data.get('case_description')

        if soc_id is None:
            soc_id = case_data.get('case_soc_id')

        if case_name is None:
            case_name = case_data.get('case_name')

        if case_tags is None:
            case_tags = case_data.get('case_tags')
        else:
            case_tags = ",".join(case_tags)

        body = {
            "case_name": case_name,
            "case_soc_id": soc_id,
            "case_description": case_description,
            "custom_attributes": custom_attributes,
            "case_tags": case_tags
        }

        resp = self._s.pi_post(f'manage/cases/update', data=body, cid=case_id)

        return resp

    def reopen_case(self, case_id: int) -> ApiResponse:
        """Reopens a case based on its ID

        Args:
          case_id: Case ID to open

        Returns:
          ApiResponse

        """
        resp = self._s.pi_post(f'manage/cases/reopen/{case_id}', cid=case_id)

        return resp

    def close_case(self, case_id: int) -> ApiResponse:
        """Closes a case based on its ID

        Args:
          case_id: Case ID to close

        Returns:
          ApiResponse

        """
        resp = self._s.pi_post(f'manage/cases/close/{case_id}', cid=case_id)

        return resp

    def delete_case(self, cid: int) -> ApiResponse:
        """Deletes a case based on its ID. All objects associated to the case are deleted. This includes :
            - assets,
            - iocs that are only referenced in this case
            - notes
            - summary
            - events
            - evidences
            - tasklogs

        Args:
          cid: Case to delete

        Returns:
          ApiResponse

        """
        resp = self._s.pi_post(f'manage/cases/delete/{cid}', cid=1)

        return resp

    def case_id_exists(self, cid: int) -> bool:
        """Checks if a case id is valid by probing the summary endpoint.
        This method returns true if the probe was successful. If False is returned
        it might not indicate the case doesn't exist but might be the result of a request malfunction
        (server down, invalid API token, etc).

        Args:
          cid:  Case ID to check

        Returns:
          True if case ID exists otherwise false

        """
        resp = self._s.pi_get(f'case/summary/fetch', cid=cid)
        return resp.is_success()

    def set_cid(self, cid: int) -> bool:
        """Sets the current cid for the Case instance.
        It can be override be setting the cid of each method though not recommended to keep consistency.

        Args:
          cid: Case ID

        Returns:
          Always true

        """

        self._cid = cid
        return True

    def _assert_cid(self, cid: int) -> int:
        """Verifies that the provided cid is set. This does not verify the validity of the cid.
        If an invalid CID is set, the requests are emitted but will likely fail.

        Args:
          cid: Case ID

        Returns:
          CaseID as int

        """
        if not cid and not self._cid:
            raise IrisClientException("No case ID provided. Either use cid argument or set_cid method")

        if not cid:
            cid = self._cid

        if not isinstance(cid, int):
            raise IrisClientException(f'Invalid CID type. Got {type(cid)} but was expecting int')

        return cid

    def get_summary(self, cid: int = None) -> ApiResponse:
        """
        Returns the summary of the specified case id.

        Args:
          cid: Case ID (Default value = None)

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)
        return self._s.pi_get(f'case/summary/fetch', cid=cid)

    def set_summary(self, summary_content: str = None, cid: int = None) -> ApiResponse:
        """Sets the summary of the specified case id.
        
        !!! warning
            This completely replace the current content of the summary. Any co-worker working on the summary
            will receive an overwrite order from the server. The order is immediately received by web socket. This method
            should probably be only used when setting a new case.

        Args:
          summary_content: Content of the summary to push. This will completely replace the current content (Default value = None)
          cid: Case ID (Default value = None)

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)
        body = {
            "case_description": summary_content,
            "cid": cid
        }

        return self._s.pi_post('case/summary/update', data=body)

    def list_notes_groups(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of notes groups of the target cid case

        Args:
          cid: Case ID (Default value = None)

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)
        return self._s.pi_get('case/notes/groups/list', cid=cid)

    def get_notes_group(self, group_id: int, cid: int = None) -> ApiResponse:
        """
        Returns a notes group based on its ID. The group ID needs to match the CID where it is stored.

        Args:
          group_id: Group ID to fetch
          cid:  Case ID (Default value = None)

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/notes/groups/{group_id}', cid=cid)

    def add_notes_group(self, group_title: str = None, cid: int = None) -> ApiResponse:
        """Creates a new notes group in the target cid case.
        Group_title can be an existing group, there is no uniqueness.

        Args:
          cid: Case ID
          group_title: Name of the group to add

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)
        body = {
            "group_title": group_title,
            "cid": cid
        }
        return self._s.pi_post('case/notes/groups/add', data=body)

    def update_notes_group(self, group_id: int, group_title: str, cid: int = None) -> ApiResponse:
        """Updates a notes group in the target cid case.
        `group_id` need to be an existing group in the target case.
        `group_title` can be an existing group, there is no uniqueness.

        Args:
          cid: Case ID
          group_id: Group ID to update
          group_title: Name of the group

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)
        body = {
            "group_title": group_title,
            "group_id": group_id,
            "cid": cid
        }
        return self._s.pi_post('case/notes/groups/update', data=body)

    def delete_notes_group(self, group_id: int, cid: int = None) -> ApiResponse:
        """Deletes a notes group. All notes in the target groups are deleted ! There is not way to get the notes back.
         Case ID needs to match the case where the group is stored.

        Args:
          cid: Case ID
          group_id: ID of the group

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)
        return self._s.pi_post(f'case/notes/groups/delete/{group_id}', cid=cid)

    def get_note(self, note_id: int, cid: int = None) -> ApiResponse:
        """Fetches a note. note_id needs to be a valid existing note in the target case.

        Args:
          cid: Case ID
          note_id: ID of the note to fetch

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/notes/{note_id}', cid=cid)

    def update_note(self, note_id: int, note_title: str = None, note_content: str = None,
                    custom_attributes: dict = None, cid: int = None) -> ApiResponse:
        """Updates a note. note_id needs to be a valid existing note in the target case.
        Only the content of the set fields is replaced.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          cid: Case ID
          note_id: Name of the note to update
          note_content: Content of the note
          note_title: Title of the note
          custom_attributes: Custom attributes of the note

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        note_req = self.get_note(note_id=note_id, cid=cid)
        if note_req.is_error():
            return ClientApiError(f'Unable to fetch note #{note_id} for update', msg=note_req.get_msg())

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        note = note_req.get_data()

        body = {
            "note_title": note_title if note_title else note.get('note_title'),
            "note_content": note_content if note_content else note.get('note_content'),
            "custom_attributes": custom_attributes,
            "cid": cid
        }

        return self._s.pi_post(f'case/notes/update/{note_id}', data=body)

    def delete_note(self, note_id: int, cid: int = None) -> ApiResponse:
        """Deletes a note. note_id needs to be a valid existing note in the target case.

        Args:
          cid: Case ID
          note_id: Name of the note to delete

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_post(f'case/notes/delete/{note_id}', cid=cid)

    def add_note(self, note_title: str, note_content: str, group_id: int, custom_attributes: dict = None,
                 cid: int = None) -> ApiResponse:
        """Creates a new note. Case ID and group note ID need to match the case in which the note is stored.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          cid: Case ID
          note_title: Title of the note
          note_content: Content of the note
          group_id: Target group to attach the note to
          custom_attributes: Custom attributes of the note

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "note_title": note_title,
            "note_content": note_content,
            "group_id": group_id,
            "custom_attributes": custom_attributes if custom_attributes else {},
            "cid": cid
        }

        return self._s.pi_post(f'case/notes/add', data=body)

    def search_notes(self, search_term: str, cid: int = None) -> ApiResponse:
        """Searches in notes. Case ID and group note ID need to match the case in which the notes are stored.
         Only the titles and notes ID of the matching notes are return, not the actual content.
         Use % for wildcard.

        Args:
          cid: int - Case ID
          search_term: str - Term to search in notes

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        body = {
            "search_term": search_term,
            "cid": cid
        }

        return self._s.pi_post(f'case/notes/search', data=body)

    def trigger_manual_hook(self, hook_ui_name: str, module_name: str, targets: list, target_type: str,
                            cid: int = None) -> ApiResponse:
        """Triggers a module hook call. These can only be used with manual hooks. The request is sent to the target
        module and processed asynchronously. The server replies immediately after queuing the task. Success feedback
        from this endpoint does not implies the hook processing was successful.

        Args:
            hook_ui_name: Hook name, as defined by the module on the UI
            module_name: Module associated with the hook name
            targets: List of IDs of objects to be processed
            target_type: Target type of targets
            cid: Case ID

        Returns:
            ApiResponse object
        """

        cid = self._assert_cid(cid)

        body = {
            "hook_name": "on_manual_trigger_ioc",
            "hook_ui_name": hook_ui_name,
            "module_name": module_name,
            "targets": targets,
            "type": target_type,
            "cid": cid
        }

        return self._s.pi_post(f'dim/hooks/call', data=body)

    def list_assets(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of all assets of the target case.

        Args:
          cid: int - Case ID

        Returns:
          APIResponse

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get('case/assets/list', cid=cid)

    def add_asset(self, name: str, asset_type: Union[str, int], analysis_status: Union[str, int],
                  compromise_status: Union[str, int] = None, tags: List[str] = None,
                  description: str = None, domain: str = None, ip: str = None, additional_info: str = None,
                  ioc_links: List[int] = None, custom_attributes: dict = None, cid: int = None,
                  **kwargs) -> ApiResponse:
        """Adds an asset to the target case id.
        
        If they are strings, asset_types and analysis_status are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          name: Name of the asset to add
          asset_type: Name or ID of the asset type
          description: Description of the asset
          compromise_status: Compromise status of the asset
          domain: Domain of the asset
          ip: IP of the asset
          additional_info: Additional information,
          analysis_status: Status of the analysis
          tags: List of tags
          ioc_links: List of IOC to link to this asset
          custom_attributes: Custom attributes of the asset
          kwargs: Additional arguments to pass to the API
          cid: int - Case ID

        Returns:
          APIResponse

        """
        cid = self._assert_cid(cid)

        if kwargs.get('compromised') is not None:
            warnings.warn("compromised argument is deprecated, use compromise_status instead", DeprecationWarning)

        if isinstance(asset_type, str):
            ast = AssetTypeHelper(session=self._s)
            asset_type_r = ast.lookup_asset_type_name(asset_type_name=asset_type)

            if not asset_type_r:
                return ClientApiError(msg=f'Asset type {asset_type} was not found')

            else:
                asset_type = asset_type_r

        if isinstance(analysis_status, str):
            ant = AnalysisStatusHelper(self._s)
            analysis_status_r = ant.lookup_analysis_status_name(analysis_status_name=analysis_status)

            if not analysis_status_r:
                return ClientApiError(msg=f"Analysis status {analysis_status} was not found")

            else:
                analysis_status = analysis_status_r

        if isinstance(compromise_status, str):
            csh = CompromiseStatusHelper(self._s)
            compromise_status_r = csh.lookup_compromise_status_name(compromise_status_name=compromise_status)

            if compromise_status_r is None:
                return ClientApiError(msg=f"Compromise status {compromise_status} was not found")

            else:
                compromise_status = compromise_status_r

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "asset_name": name,
            "asset_type_id": asset_type,
            "analysis_status_id": analysis_status,
            "cid": cid
        }

        if description is not None:
            body['asset_description'] = description
        if domain is not None:
            body['asset_domain'] = domain
        if ip is not None:
            body['asset_ip'] = ip
        if additional_info is not None:
            body['asset_info'] = additional_info
        if ioc_links is not None:
            body['ioc_links'] = [str(ioc) for ioc in ioc_links]
        if compromise_status is not None:
            body['asset_compromise_status_id'] = compromise_status
        if tags is not None:
            body['asset_tags'] = ','.join(tags)
        if custom_attributes is not None:
            body['custom_attributes'] = custom_attributes

        return self._s.pi_post(f'case/assets/add', data=body)

    def get_asset(self, asset_id: int, cid: int = None) -> ApiResponse:
        """
        Returns an asset information from its ID.

        Args:
          asset_id: ID of the asset to fetch
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/assets/{asset_id}', cid=cid)

    def asset_exists(self, asset_id: int, cid: int = None) -> bool:
        """
        Returns true if asset_id exists in the context of the current case or cid.
        This method is an overlay of get_asset and thus not performant.

        Args:
          asset_id: Asset to lookup
          cid: Case ID

        Returns:
          True if exists else false

        """
        cid = self._assert_cid(cid)
        resp = self.get_asset(asset_id=asset_id, cid=cid)

        return resp.is_success()

    def update_asset(self, asset_id: int, name: str = None, asset_type: Union[str, int] = None, tags: List[str] = None,
                     analysis_status: Union[str, int] = None, description: str = None, domain: str = None,
                     ip: str = None, additional_info: str = None, ioc_links: List[int] = None,
                     compromise_status: Union[str, int] = None,
                     custom_attributes: dict = None, cid: int = None, no_sync=False, **kwargs) -> ApiResponse:
        """
        Updates an asset. asset_id needs to be an existing asset in the target case cid.
        
        If they are strings, asset_types and analysis_status are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          asset_id: ID of the asset to update
          name: Name of the asset
          asset_type: Name or ID of the asset type
          tags: List of tags
          description: Description of the asset
          domain: Domain of the asset
          ip: IP of the asset
          additional_info: Additional information,
          analysis_status: Status of the analysis
          ioc_links: List of IOC to link to this asset
          compromise_status: Status of the compromise
          custom_attributes: Custom attributes of the asset
          cid: Case ID


        Returns:
          APIResponse

        """
        cid = self._assert_cid(cid)

        if kwargs.get('compromised') is not None:
            warnings.warn("compromised argument is deprecated, use compromise_status instead", DeprecationWarning)

        asset = None
        if not no_sync:
            asset_req = self.get_asset(asset_id=asset_id, cid=cid)
            if asset_req.is_error():
                return asset_req

            asset = asset_req.get_data()

        if isinstance(asset_type, str):
            ast = AssetTypeHelper(session=self._s)
            asset_type_r = ast.lookup_asset_type_name(asset_type_name=asset_type)

            if not asset_type_r:
                return ClientApiError(msg=f'Asset type {asset_type} not found')

            else:
                asset_type = asset_type_r

        if isinstance(compromise_status, str):
            csh = CompromiseStatusHelper(self._s)
            compromise_status_r = csh.lookup_compromise_status_name(compromise_status_name=compromise_status)

            if compromise_status_r is None:
                return ClientApiError(msg=f"Compromise status {compromise_status} was not found")

            else:
                compromise_status = compromise_status_r

        if isinstance(analysis_status, str):
            ant = AnalysisStatusHelper(self._s)
            analysis_status_r = ant.lookup_analysis_status_name(analysis_status_name=analysis_status)

            if not analysis_status_r:
                return ClientApiError(msg=f"Analysis status {analysis_status} not found")

            else:
                analysis_status = analysis_status_r

        if ioc_links:
            for link in ioc_links:
                ioc = self.get_ioc(ioc_id=int(link))
                if ioc.is_error():
                    return ClientApiError(msg=f"IOC {link} was not found", error=ioc.get_data())

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "asset_name": name if name is not None or no_sync else asset.get('asset_name'),
            "asset_type_id": asset_type if asset_type is not None or no_sync else int(asset.get('asset_type_id')),
            "analysis_status_id": analysis_status if analysis_status is not None or no_sync else int(
                asset.get('analysis_status_id')),
            "asset_description": description if description is not None or no_sync else asset.get('analysis_status'),
            "asset_domain": domain if domain is not None or no_sync else asset.get('asset_domain'),
            "asset_ip": ip if ip is not None or no_sync else asset.get('asset_ip'),
            "asset_info": additional_info if additional_info is not None or no_sync else asset.get('asset_info'),
            "asset_compromise_status_id": compromise_status if compromise_status is not None or no_sync else int(
                asset.get('asset_compromise_status_id')),
            "asset_tags": ','.join(tags) if tags is not None or no_sync else asset.get('asset_tags'),
            "custom_attributes": custom_attributes if custom_attributes else asset.get('custom_attributes'),
            "cid": cid
        }

        if ioc_links is not None:
            body['ioc_links'] = [str(ioc) for ioc in ioc_links]

        return self._s.pi_post(f'case/assets/update/{asset_id}', data=body)

    def delete_asset(self, asset_id: int, cid: int = None) -> ApiResponse:
        """Deletes an asset identified by asset_id. CID must match the case in which the asset is stored.

        Args:
          asset_id: ID of the asset to delete
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_post(f'case/assets/delete/{asset_id}', cid=cid)

    def list_iocs(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of all iocs of the target case.

        Args:
          cid: Case ID

        Returns:
          APIResponse

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get('case/ioc/list', cid=cid)

    def add_ioc(self, value: str, ioc_type: Union[str, int], description: str = None,
                ioc_tlp: Union[str, int] = None, ioc_tags: list = None, custom_attributes: dict = None,
                cid: int = None) -> ApiResponse:
        """
        Adds an ioc to the target case id.
        
        If they are strings, ioc_tlp and ioc_type are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          value: Value of the IOC
          ioc_type: Type of IOC, either name or type ID
          description: Optional - Description of the IOC
          ioc_tlp: TLP name or tlp ID. Default is orange
          ioc_tags: List of tags to add
          custom_attributes: Custom attributes of the ioc
          cid: Case ID

        Returns:
          APIResponse

        """
        cid = self._assert_cid(cid)

        if ioc_tlp and isinstance(ioc_tlp, str):
            tlp = TlpHelper(session=self._s)
            ioc_tlp_r = tlp.lookup_tlp_name(tlp_name=ioc_tlp)

            if not ioc_tlp_r:
                return ClientApiError(msg=f"TLP {ioc_tlp} is invalid")

            ioc_tlp = ioc_tlp_r

        if ioc_type and isinstance(ioc_type, str):
            ioct = IocTypeHelper(session=self._s)
            ioct_r = ioct.lookup_ioc_type_name(ioc_type_name=ioc_type)

            if not ioct_r:
                return ClientApiError(msg=f"IOC type {ioc_type} is invalid", error=ioct_r)

            ioc_type = ioct_r

        if ioc_tags and not isinstance(ioc_tags, list):
            return ClientApiError(f"IOC tags must be a list of str")

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "ioc_value": value,
            "ioc_tlp_id": ioc_tlp if ioc_tlp else 2,
            "ioc_type_id": ioc_type,
            "custom_attributes": custom_attributes if custom_attributes else {},
            "cid": cid
        }

        if description:
            body['ioc_description'] = description
        if ioc_tags:
            body['ioc_tags'] = ",".join(ioc_tags)

        return self._s.pi_post(f'case/ioc/add', data=body)

    def get_ioc(self, ioc_id: int, cid: int = None) -> ApiResponse:
        """
        Returns an IOC.  ioc_id needs to be an existing ioc in the provided case ID.

        Args:
          ioc_id: IOC ID
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/ioc/{ioc_id}', cid=cid)

    def update_ioc(self, ioc_id: int, value: str = None, ioc_type: Union[str, int] = None, description: str = None,
                   ioc_tlp: Union[str, int] = None, ioc_tags: list = None, custom_attributes: dict = None,
                   cid: int = None) -> ApiResponse:
        """
        Updates an existing IOC. ioc_id needs to be an existing ioc in the provided case ID.
        
        If they are strings, ioc_tlp and ioc_type are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          ioc_id: IOC ID to update
          value: Value of the IOC
          ioc_type: Type of IOC, either name or type ID
          description: Description of the IOC
          ioc_tlp: TLP name or tlp ID. Default is orange
          ioc_tags: List of tags to add,
          custom_attributes: Custom attributes of the IOC
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        ioc_req = self.get_ioc(ioc_id, cid=cid)
        if ioc_req.is_error():
            return ClientApiError(msg=f'Unable to fetch IOC #{ioc_id} for update', error=ioc_req.get_msg())

        ioc = ioc_req.get_data()

        if ioc_tlp and isinstance(ioc_tlp, str):
            tlp = TlpHelper(session=self._s)
            ioc_tlp_r = tlp.lookup_tlp_name(tlp_name=ioc_tlp)

            if not ioc_tlp_r:
                return ClientApiError(msg=f"TLP {ioc_tlp} is invalid")

            ioc_tlp = ioc_tlp_r

        if ioc_type and isinstance(ioc_type, str):
            ioct = IocTypeHelper(session=self._s)
            ioct_r = ioct.lookup_ioc_type_name(ioc_type_name=ioc_type)

            if not ioct_r:
                return ClientApiError(msg=f"IOC type {ioc_type} is invalid", error=ioct_r)

            ioc_type = ioct_r

        if ioc_tags and not isinstance(ioc_tags, list):
            return ClientApiError(f"IOC tags must be a list of str")

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "ioc_value": value if value else ioc.get('ioc_value'),
            "ioc_tlp_id": ioc_tlp if ioc_tlp else int(ioc.get('ioc_tlp_id')),
            "ioc_type_id": ioc_type if ioc_type else int(ioc.get('ioc_type_id')),
            "ioc_description": description if description else ioc.get('ioc_description'),
            "ioc_tags": ",".join(ioc_tags) if ioc_tags else ioc.get('ioc_tags'),
            "custom_attributes": custom_attributes if custom_attributes else ioc.get('custom_attributes'),
            "cid": cid
        }

        return self._s.pi_post(f'case/ioc/update/{ioc_id}', data=body)

    def delete_ioc(self, ioc_id: int, cid: int = None) -> ApiResponse:
        """
        Deletes an IOC from its ID. CID must match the case in which the ioc is stored.

        Args:
          ioc_id: ID of the ioc
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_post(f'case/ioc/delete/{ioc_id}', cid=cid)

    def get_event(self, event_id: int, cid: int = None) -> ApiResponse:
        """
        Returns an event from the timeline

        Args:
          event_id: ID of the event to fetch
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/timeline/events/{event_id}', cid=cid)

    def list_events(self, filter_by_asset: int = 0, cid: int = None) -> ApiResponse:
        """
        Returns a list of events from the timeline. filter_by_asset can be used to return only the events
        linked to a specific asset. In case the asset doesn't exist, an empty timeline is returned.

        Args:
          filter_by_asset: Select the timeline of a specific asset by setting an existing asset ID
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/timeline/events/list/filter/{filter_by_asset}', cid=cid)

    def filter_events(self, filter_str: dict = None, cid: int = None) -> ApiResponse:
        """
        Returns a list of events from the timeline, filtered with the same query types used in
        the UI.

        Args:
          filter_str: Filter the timeline as in the UI
          cid: Case ID

        Returns:
          APIResponse object
        """
        cid = self._assert_cid(cid)

        filter_str = {} if filter_str is None else filter_str
        filter_uri = urllib.parse.quote(json.dumps(filter_str))

        return self._s.pi_get(f'case/timeline/advanced-filter?q={filter_uri}&', cid=cid)

    def add_event(self, title: str, date_time: datetime, content: str = None, raw_content: str = None,
                  source: str = None, linked_assets: list = None, linked_iocs: list = None,
                  category: Union[int, str] = None, tags: list = None, color: str = None, display_in_graph: bool = None,
                  display_in_summary: bool = None, custom_attributes: str = None, timezone_string: str = None,
                  sync_ioc_with_assets: bool = False, cid: int = None) -> ApiResponse:
        """
        Adds a new event to the timeline.
        
        If it is a string, category is lookup-ed up before the addition request is issued.
        it can be either a name or an ID. For performances prefer an ID as it is used directly in the request
        without prior lookup.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          title: Title of the event
          date_time: Datetime of the event, including timezone
          content: Content of the event (displayed in timeline on GUI)
          raw_content: Raw content of the event (displayed in detailed event on GUI)
          source: Source of the event
          linked_assets: List of assets to link with this event
          linked_iocs: List of IOCs to link with this event
          category: Category of the event (MITRE ATT@CK)
          color: Left border of the event in the timeline
          display_in_graph: Set to true to display in graph page - Default to true
          display_in_summary: Set to true to display in Summary - Default to false
          tags: A list of strings to add as tags
          custom_attributes: Custom attributes of the event
          timezone_string: Timezone in format +XX:XX or -XX:XX. If none, +00:00 is used
          sync_ioc_with_assets: Set to true to sync the IOC with the assets
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        if category and isinstance(category, str):
            cat = EventCategoryHelper(session=self._s)
            evtx_cat_r = cat.lookup_event_category_name(event_category=category)

            if not evtx_cat_r:
                return ClientApiError(msg=f"Event category {category} is invalid")

            category = evtx_cat_r

        if not isinstance(date_time, datetime.datetime):
            return ClientApiError(msg=f"Expected datetime object for date_time but got {type(date_time)}")

        if tags and not isinstance(tags, list):
            return ClientApiError(msg=f"Expected list object for tags but got {type(tags)}")

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "event_title": title,
            "event_in_graph": display_in_graph if display_in_graph is not None else True,
            "event_in_summary": display_in_summary if display_in_summary is not None else False,
            "event_content": content if content else "",
            "event_raw": raw_content if raw_content else "",
            "event_source": source if source else "",
            "event_assets": linked_assets if linked_assets else [],
            "event_iocs": linked_iocs if linked_iocs else [],
            "event_category_id": category if category else "1",
            "event_color": color if color else "",
            "event_date": date_time.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            "event_tags": ','.join(tags) if tags else '',
            "event_tz": timezone_string if timezone_string else "+00:00",
            "custom_attributes": custom_attributes if custom_attributes else {},
            "event_sync_iocs_assets": sync_ioc_with_assets if sync_ioc_with_assets is True else False,
            "cid": cid
        }

        return self._s.pi_post(f'case/timeline/events/add', data=body)

    def update_event(self, event_id: int, title: str = None, date_time: datetime = None, content: str = None,
                     raw_content: str = None, source: str = None, linked_assets: list = None, linked_iocs: list = None,
                     category: Union[int, str] = None, tags: list = None,
                     color: str = None, display_in_graph: bool = None, display_in_summary: bool = None,
                     custom_attributes: dict = None, cid: int = None, timezone_string: str = None,
                     sync_ioc_with_assets: bool = False) -> ApiResponse:
        """
        Updates an event of the timeline. event_id needs to be an existing event in the target case.
        
        If it is a string, category is lookup-ed up before the addition request is issued.
        it can be either a name or an ID. For performances prefer an ID as it is used directly in the request
        without prior lookup.
        
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          event_id: Event ID to update
          title: Title of the event
          date_time: Datetime of the event, including timezone
          content: Content of the event (displayed in timeline on GUI)
          raw_content: Raw content of the event (displayed in detailed event on GUI)
          source: Source of the event
          linked_assets: List of assets to link with this event
          linked_iocs: List of IOCs to link with this event
          category: Category of the event (MITRE ATT@CK)
          color: Left border of the event in the timeline
          display_in_graph: Set to true to display in graph page - Default to true
          display_in_summary: Set to true to display in Summary - Default to false
          tags: A list of strings to add as tags
          custom_attributes: Custom attributes of the event
          timezone_string: Timezone in format +XX:XX or -XX:XX. If none, +00:00 is used
          sync_ioc_with_assets: Set to true to sync the IOC with the assets
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        event_req = self.get_event(event_id, cid=cid)
        if event_req.is_error():
            return ClientApiError(msg=event_req.get_msg())

        event = event_req.get_data()

        if category and isinstance(category, str):
            cat = EventCategoryHelper(session=self._s)
            evtx_cat_r = cat.lookup_event_category_name(event_category=category)

            if not evtx_cat_r:
                return ClientApiError(msg=f"Event category {category} is invalid")

            category = evtx_cat_r

        if date_time and not isinstance(date_time, datetime.datetime):
            return ClientApiError(msg=f"Expected datetime object for date_time but got {type(date_time)}")

        if tags and not isinstance(tags, list):
            return ClientApiError(msg=f"Expected list object for tags but got {type(tags)}")

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "event_title": title if title else event.get('event_title'),
            "event_in_graph": display_in_graph if display_in_graph is not None else event.get('event_in_graph'),
            "event_in_summary": display_in_summary if display_in_summary is not None else event.get('event_in_summary'),
            "event_content": content if content else event.get('event_content'),
            "event_raw": raw_content if raw_content else event.get('event_raw'),
            "event_source": source if source else event.get('event_source'),
            "event_assets": linked_assets if linked_assets else [],
            "event_iocs": linked_iocs if linked_iocs else [],
            "event_category_id": category if category else event.get('event_category_id'),
            "event_color": color if color else event.get('event_color'),
            "event_date": date_time.strftime('%Y-%m-%dT%H:%M:%S.%f') if date_time else event.get('event_date'),
            "event_tags": ','.join(tags) if tags else event.get('event_tags'),
            "event_tz": timezone_string if timezone_string else event.get('event_tz'),
            "custom_attributes": custom_attributes if custom_attributes else event.get('custom_attributes'),
            "event_sync_iocs_assets": sync_ioc_with_assets if sync_ioc_with_assets is True else False,
            "cid": cid
        }

        return self._s.pi_post(f'case/timeline/events/update/{event_id}', data=body)

    def delete_event(self, event_id: int, cid: int = None) -> ApiResponse:
        """
        Deletes an event from its ID. CID must match the case in which the event is stored

        Args:
          event_id: Event to delete
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_post(f'case/timeline/events/delete/{event_id}', cid=cid)

    def add_task_log(self, message: str, cid: int = None) -> ApiResponse:
        """
        Adds a new task log that will appear under activities

        Args:
          message: Message to log
          cid: Case ID

        Returns:
          ApiResponse

        """
        cid = self._assert_cid(cid)
        data = {
            "log_content": message,
            "cid": cid
        }

        return self._s.pi_post(f'case/tasklog/add', data=data)

    def list_tasks(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of tasks linked to the provided case.

        Args:
          cid: Case ID

        Returns:
          ApiResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/tasks/list', cid=cid)

    def get_task(self, task_id: int, cid: int = None) -> ApiResponse:
        """
        Returns a task from its ID. task_id needs to be a valid task in the target case.

        Args:
          task_id: Task ID to lookup
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/tasks/{task_id}', cid=cid)

    def add_task(self, title: str, status: Union[str, int], assignees: List[Union[str, int]], description: str = None,
                 tags: list = None, custom_attributes: dict = None, cid: int = None) -> ApiResponse:
        """
        Adds a new task to the target case.
        
        If they are strings, status and assignee are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          title: Title of the task
          description: Description of the task
          assignees: List of assignees ID or username
          cid: Case ID
          tags: Tags of the task
          status: String or status ID, need to be a valid status
          custom_attributes: Custom attributes of the task

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)
        assignees_list = []

        for assignee in assignees:
            if isinstance(assignee, str):
                user = User(self._s)
                assignee_r = user.lookup_username(username=assignee)
                if assignee_r.is_error():
                    return assignee_r

                assignee = assignee_r.get_data().get('user_id')
                if not assignee:
                    return ClientApiError(msg=f'Error while looking up username {assignee}')

            elif not isinstance(assignee, int):
                return ClientApiError(msg=f'Invalid assignee type {type(assignee)}')

            assignees_list.append(assignee)

        if isinstance(status, str):
            tsh = TaskStatusHelper(self._s)
            tsh_r = tsh.lookup_task_status_name(task_status_name=status)
            if tsh_r is None:
                return ClientApiError(msg=f'Invalid task status {status}')
            status = tsh_r

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "task_assignees_id": assignees_list,
            "task_description": description if description else "",
            "task_status_id": status,
            "task_tags": ','.join(tags) if tags else "",
            "task_title": title,
            "custom_attributes": custom_attributes if custom_attributes else {},
            "cid": cid
        }

        return self._s.pi_post(f'case/tasks/add', data=body)

    def update_task(self, task_id: int, title: str = None, status: Union[str, int] = None,
                    assignees: List[Union[int, str]] = None, description: str = None, tags: list = None,
                    custom_attributes: dict = None, cid: int = None) -> ApiResponse:
        """
        Updates a task. task_id needs to be a valid task in the target case.
        
        If they are strings, status and assignee are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          task_id: ID of the task to update
          title: Title of the task
          description: Description of the task
          assignees: List of assignee ID or assignee username
          cid: Case ID
          tags: Tags of the task
          status: String status, need to be a valid status
          custom_attributes: Custom attributes of the task

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        task_req = self.get_task(task_id=task_id)

        if task_req.is_error():
            return ClientApiError(msg=f'Unable to fetch task #{task_id} for update', error=task_req.get_msg())

        assignees_list = []
        if assignees:
            for assignee in assignees:
                if assignee and isinstance(assignee, str):
                    user = User(self._s)
                    assignee_r = user.lookup_username(username=assignee)
                    if assignee_r.is_error():
                        return assignee_r

                    assignee = assignee_r.get_data().get('user_id')
                    if not assignee:
                        return ClientApiError(msg=f'Error while looking up username {assignee}')

                elif assignee and not isinstance(assignee, int):
                    return ClientApiError(msg=f'Invalid assignee type {type(assignee)}')

                assignees_list.append(assignee)

        if status and isinstance(status, str):
            tsh = TaskStatusHelper(self._s)
            tsh_r = tsh.lookup_task_status_name(task_status_name=status)
            if tsh_r is None:
                return ClientApiError(msg=f'Invalid task status {status}')
            status = tsh_r

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        task = task_req.get_data()

        if not assignees_list:
            assignees_list = [u.get('id') for u in task.get('task_assignees')]

        body = {
            "task_assignees_id": assignees_list,
            "task_description": description if description else task.get('task_description'),
            "task_status_id": status if status else task.get('task_status_id'),
            "task_tags": ",".join(tags) if tags else task.get('task_tags'),
            "task_title": title if title else task.get('task_title'),
            "custom_attributes": custom_attributes if custom_attributes else task.get('custom_attributes'),
            "cid": cid
        }

        return self._s.pi_post(f'case/tasks/update/{task_id}', data=body)

    def delete_task(self, task_id: int, cid: int = None) -> ApiResponse:
        """
        Deletes a task from its ID. CID must match the case in which the task is stored.

        Args:
          task_id: Task to delete
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_post(f'case/tasks/delete/{task_id}', cid=cid)

    def list_evidences(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of evidences.

        Args:
          cid: Case ID

        Returns:
          ApiResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/evidences/list', cid=cid)

    def get_evidence(self, evidence_id: int, cid: int = None) -> ApiResponse:
        """
        Returns an evidence from its ID. evidence_id needs to be an existing evidence in the target case.

        Args:
          evidence_id: Evidence ID to lookup
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/evidences/{evidence_id}', cid=cid)

    def add_evidence(self, filename: str, file_size: int, description: str = None,
                     file_hash: str = None, custom_attributes: dict = None, cid: int = None) -> ApiResponse:
        """
        Adds a new evidence to the target case.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          filename: name of the evidence
          file_size: Size of the file
          description: Description of the evidence
          file_hash: hash of the evidence
          custom_attributes: Custom attributes of the evidences
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "filename": filename,
            "file_size": file_size,
            "file_description": description,
            "file_hash": file_hash,
            "custom_attributes": custom_attributes if custom_attributes else {},
            "cid": cid
        }

        return self._s.pi_post(f'case/evidences/add', data=body)

    def update_evidence(self, evidence_id: int, filename: str = None, file_size: int = None, description: str = None,
                        file_hash: str = None, custom_attributes: dict = None, cid: int = None) -> ApiResponse:
        """
        Updates an evidence of the matching case. evidence_id needs to be an existing evidence in the target case.
        
        Custom_attributes is an undefined structure when the call is made. This method does not
        allow to push a new attribute structure. The submitted structure must follow the one defined
        by administrators in the UI otherwise it is ignored.

        Args:
          evidence_id: ID of the evidence
          filename: name of the evidence
          file_size: Size of the file
          description: Description of the evidence
          file_hash: hash of the evidence
          custom_attributes: custom attributes of the evidences
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        evidence_req = self.get_evidence(evidence_id=evidence_id, cid=cid)
        if evidence_req.is_error():
            return ClientApiError(msg=f'Unable to fetch evidence #{evidence_id} for update',
                                  error=evidence_req.get_msg())

        evidence = evidence_req.get_data()

        if custom_attributes is not None and not isinstance(custom_attributes, dict):
            return ClientApiError(f'Got type {type(custom_attributes)} for custom_attributes but dict was expected.')

        body = {
            "filename": filename if filename else evidence.get('filename'),
            "file_size": file_size if file_size else evidence.get('file_size'),
            "file_description": description if description else evidence.get('file_description'),
            "file_hash": file_hash if file_hash else evidence.get('file_hash'),
            "custom_attributes": custom_attributes if custom_attributes else evidence.get("custom_attributes"),
            "cid": cid
        }

        return self._s.pi_post(f'case/evidences/update/{evidence_id}', data=body)

    def delete_evidence(self, evidence_id: int, cid: int = None):
        """
        Deletes an evidence from its ID. evidence_id needs to be an existing evidence in the target case.

        Args:
          evidence_id: int - Evidence to delete
          cid: int - Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_post(f'case/evidences/delete/{evidence_id}', cid=cid)

    def list_global_tasks(self) -> ApiResponse:
        """

        Args:

        Returns:
          :return: ApiResponse object

        """
        return self._s.pi_get(f'global/tasks/list', cid=1)

    def get_global_task(self, task_id: int) -> ApiResponse:
        """
        Returns a global task from its ID.

        Args:
          task_id: Task ID to lookup

        Returns:
          APIResponse object

        """

        return self._s.pi_get(f'global/tasks/{task_id}', cid=1)

    def add_global_task(self, title: str, status: Union[str, int], assignee: Union[str, int], description: str = None,
                        tags: list = None) -> ApiResponse:
        """
        Adds a new task.
        
        If set as strings, status and assignee are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as it is used directly in the request
        without prior lookup.

        Args:
          title: Title of the task
          description: Description of the task
          assignee: Assignee ID or username
          tags: Tags of the task
          status: String or status ID, need to be a valid status

        Returns:
          APIResponse object

        """

        if isinstance(assignee, str):
            user = User(self._s)
            assignee_r = user.lookup_username(username=assignee)
            if assignee_r.is_error():
                return assignee_r

            assignee = assignee_r.get_data().get('user_id')
            if not assignee:
                return ClientApiError(msg=f'Error while looking up username {assignee}')

        elif not isinstance(assignee, int):
            return ClientApiError(msg=f'Invalid assignee type {type(assignee)}')

        if status and isinstance(status, str):
            tsh = TaskStatusHelper(self._s)
            tsh_r = tsh.lookup_task_status_name(task_status_name=status)
            if tsh_r is None:
                return ClientApiError(msg=f'Invalid task status {status}')
            status = tsh_r

        body = {
            "task_assignee_id": assignee,
            "task_description": description if description else "",
            "task_status_id": status,
            "task_tags": ','.join(tags) if tags else "",
            "task_title": title,
            "cid": 1
        }

        return self._s.pi_post(f'global/tasks/add', data=body)

    def update_global_task(self, task_id: int, title: str = None, status: Union[str, int] = None,
                           assignee: Union[int, str] = None, description: str = None,
                           tags: list = None) -> ApiResponse:
        """
        Updates a task. task_id needs to be an existing task in the database.
        
        If they are strings, status and assignee are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.

        Args:
          task_id: ID of the task to update
          title: Title of the task
          description: Description of the task
          assignee: Assignee ID or assignee username
          tags: Tags of the task
          status: String status, need to be a valid status

        Returns:
          APIResponse object

        """

        task_req = self.get_global_task(task_id=task_id)

        if task_req.is_error():
            return ClientApiError(msg=f'Unable to fetch task #{task_id} for update', error=task_req.get_msg())

        if assignee and isinstance(assignee, str):
            user = User(self._s)
            assignee_r = user.lookup_username(username=assignee)
            if assignee_r.is_error():
                return assignee_r

            assignee = assignee_r.get_data().get('user_id')
            if not assignee:
                return ClientApiError(msg=f'Error while looking up username {assignee}')

        elif assignee and not isinstance(assignee, int):
            return ClientApiError(msg=f'Invalid assignee type {type(assignee)}')

        if status and isinstance(status, str):
            tsh = TaskStatusHelper(self._s)
            tsh_r = tsh.lookup_task_status_name(task_status_name=status)
            if tsh_r is None:
                return ClientApiError(msg=f'Invalid task status {status}')
            status = tsh_r

        task = task_req.get_data()

        body = {
            "task_assignee_id": assignee if assignee else task.get('task_assignee_id'),
            "task_description": description if description else task.get('task_description'),
            "task_status_id": status if status else task.get('task_status_id'),
            "task_tags": ",".join(tags) if tags else task.get('task_tags'),
            "task_title": title if title else task.get('task_title'),
        }

        return self._s.pi_post(f'global/tasks/update/{task_id}', data=body)

    def delete_global_task(self, task_id: int) -> ApiResponse:
        """
        Deletes a global task from its ID. task_id needs to be an existing task in the database.

        Args:
          task_id: int - Task to delete

        Returns:
          APIResponse object

        """

        return self._s.pi_post(f'global/tasks/delete/{task_id}', cid=1)

    def list_ds_tree(self, cid: int = None) -> ApiResponse:
        """
        Returns the tree of the Datastore

        Args:
          cid: Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'datastore/list/tree', cid=cid)

    def add_ds_file(self, parent_id: int, file_stream: BinaryIO, filename: str, file_description: str,
                    file_is_ioc: bool = False, file_is_evidence: bool = False, file_password: str = None,
                    file_tags: list[str] = None, cid: int = None) -> ApiResponse:
        """
        Adds a file to the Datastore.

        Args:
          file_stream: BinaryIO - File stream to upload
          filename: str - File name
          file_description: str - File description
          file_is_ioc: bool - Is the file an IOC
          file_is_evidence: bool - Is the file an evidence
          parent_id: int - Parent ID
          file_password: str - File password
          file_tags: str - File tags
          cid: int - Case ID

        Returns:
          APIResponse object

        """
        cid = self._assert_cid(cid)

        files = {
            'file_content': (filename, file_stream)
        }

        data = {
            'file_original_name': filename,
            'file_password': file_password if file_password else '',
            'file_is_ioc': 'y' if file_is_ioc else 'n',
            'file_is_evidence': 'y' if file_is_evidence else 'n',
            'file_description': file_description,
            'file_tags': ','.join(file_tags) if file_tags else ''
        }

        return self._s.pi_post_files(f'datastore/file/add/{parent_id}', files=files, data=data, cid=cid)

    def get_ds_file_info(self, file_id: int, cid: int = None) -> ApiResponse:
        """
        Returns information from file of the Datastore.

        Args:
            file_id: int - File ID
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'datastore/file/info/{file_id}', cid=cid)

    def update_ds_file(self, file_id: int, file_name: str = None, file_description: str = None,
                       file_is_ioc: bool = False, file_is_evidence: bool = False, file_password: str = None,
                       file_tags: list[str] = None,
                       cid: int = None) -> ApiResponse:
        """
        Updates a file in the Datastore.

        Args:
            file_id: int - File ID
            file_name: str - File name
            file_description: str - File description
            file_is_ioc: bool - Is the file an IOC
            file_is_evidence: bool - Is the file an evidence
            file_password: str - File password
            file_tags: str - File tags
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        ds_file_req = self.get_ds_file_info(file_id=file_id, cid=cid)
        if ds_file_req.is_error():
            return ds_file_req

        ds_file = get_data_from_resp(ds_file_req)

        if file_is_ioc is None:
            file_is_ioc = ds_file.get('file_is_ioc')

        if file_is_evidence is None:
            file_is_evidence = ds_file.get('file_is_evidence')

        data = {
            'file_original_name': file_name if file_name is not None else ds_file.get('file_original_name'),
            'file_password': file_password if file_password is not None else ds_file.get('file_password'),
            'file_is_ioc': 'y' if file_is_ioc else 'n',
            'file_is_evidence': 'y' if file_is_evidence else 'n',
            'file_description': file_description if file_description is not None else ds_file.get('file_description'),
            'file_tags': ','.join(file_tags) if file_tags is not None else ds_file.get('file_tags')
        }

        return self._s.pi_post_files(f'datastore/file/update/{file_id}', data=data, cid=cid)

    def delete_ds_file(self, file_id: int, cid: int = None) -> ApiResponse:
        """
        Deletes a file from the Datastore.

        Args:
            file_id: int - File ID
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_post(f'datastore/file/delete/{file_id}', cid=cid)

    def download_ds_file(self, file_id: int, cid: int = None) -> Response:
        """
        Downloads a file from the Datastore.

        Args:
            file_id: int - File ID
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'datastore/file/view/{file_id}', cid=cid, no_wrap=True)

    def move_ds_file(self, file_id: int, parent_id: int, cid: int = None) -> ApiResponse:
        """
        Moves a file from a folder to another.

        Args:
            file_id: int - File ID
            parent_id: int - New parent ID
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        data = {
            'destination-node': parent_id
        }

        return self._s.pi_post(f'datastore/file/move/{file_id}', data=data, cid=cid)

    def add_ds_folder(self, parent_id: int, folder_name: str, cid: int = None) -> ApiResponse:
        """
        Adds a folder to the Datastore.

        Args:
            parent_id: int - Parent ID
            folder_name: str - Folder name
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        data = {
            'parent_node': parent_id,
            'folder_name': folder_name
        }

        return self._s.pi_post(f'datastore/folder/add', data=data, cid=cid)

    def delete_ds_folder(self, folder_id: int, cid: int = None) -> ApiResponse:
        """
        Deletes a folder from the Datastore.

        Args:
            folder_id: int - Folder ID
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        return self._s.pi_post(f'datastore/folder/delete/{folder_id}', cid=cid)

    def rename_ds_folder(self, folder_id: int, new_name: str, cid: int = None) -> ApiResponse:
        """
        Renames a folder in the Datastore.

        Args:
            folder_id: int - Folder ID
            new_name: str - New name
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        data = {
            'folder_name': new_name,
            'parent_node': folder_id
        }

        return self._s.pi_post(f'datastore/folder/rename/{folder_id}', data=data, cid=cid)

    def move_ds_folder(self, folder_id: int, parent_id: int, cid: int = None) -> ApiResponse:
        """
        Moves a folder from a folder to another.

        Args:
            folder_id: int - Folder ID
            parent_id: int - New parent ID
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        data = {
            'destination-node': parent_id
        }

        return self._s.pi_post(f'datastore/folder/move/{folder_id}', data=data, cid=cid)

    def add_asset_comment(self, asset_id: int, comment: str, cid: int = None) -> ApiResponse:
        """
        Adds a comment to an asset.

        Args:
            asset_id: int - Asset ID
            comment: str - Comment
            cid: int - Case ID

        Returns:
            APIResponse object

        """
        cid = self._assert_cid(cid)

        data = {
            'comment_text': comment
        }

        return self._s.pi_post(f'case/assets/{asset_id}/comments/add', data=data, cid=cid)

