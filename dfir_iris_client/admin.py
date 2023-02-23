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
import warnings
from typing import List
from typing import Union
from deprecated import deprecated

from dfir_iris_client.helper.assets_type import AssetTypeHelper
from dfir_iris_client.customer import Customer
from dfir_iris_client.helper.authorization import Permissions
from dfir_iris_client.helper.ioc_types import IocTypeHelper
from dfir_iris_client.helper.utils import ApiResponse, ClientApiError, get_data_from_resp, parse_api_data, ClientApiData


class AdminHelper(object):
    """Handles administrative tasks"""
    def __init__(self, session):
        """
        Overlay offering administrative tasks. Initialisation of the class does NOT check if the calling user
        has admin rights anymore. If the user doesn't, 403 will be generated upon requests

        Args:
            session: ClientSession object

        """
        self._s = session

    @deprecated('Use the new has_permission(<permission>) method', version="2.0.0", action="error")
    def is_user_admin(self) -> bool:
        """
        Deprecated in IRIS v1.5.0. Use the new has_permission(<permission>) method.
        Returns True if the calling user is administrator

        Args:

        Returns:
            Bool - true if the calling is administrator

        """
        req = self._s.pi_get('user/is-admin')
        return req.is_success()

    def has_permission(self, permission: Permissions) -> ApiResponse:
        """
        Returns true if the user has the given permissions

        Args:
            permission: Permission to check

        Returns:
            ApiResponse
        """
        body = {
            "permission_name": permission.name,
            "permission_value": permission.value
        }

        req = self._s.pi_post('user/has-permission', data=body, cid=1)
        return req

    def get_user(self, login: str) -> ApiResponse:
        """
        Returns a user by its login. Login names are unique in Iris.

        Args:
          login: username to lookup

        Returns:
          ApiResponse

        """

        user_lookup_r = self._s.pi_get(f'manage/users/lookup/login/{login}', cid=1)
        if user_lookup_r.is_error():
            return ClientApiError(msg=user_lookup_r.get_msg())

        user_id = user_lookup_r.get_data().get('user_id')

        return self._s.pi_get(f'manage/users/{user_id}')

    def add_user(self, login: str, name: str, password: str, email: str, **kwargs) -> ApiResponse:
        """
        Adds a new user. A new user can be successfully added if
        
        - login is unique
        - email is unique
        - password meets the requirements of IRIS
        
        !!! tip "Requires server administrator rights"

        Args:
          login: Username (login name) of the user to add
          name: Full name of the user
          password: Password of the user
          email: Email of the user

        Returns:
          ApiResponse

        """
        body = {
            "user_login": login,
            "user_name": name,
            "user_password": password,
            "user_email": email,
            "cid": 1
        }

        if kwargs.get('is_admin') is not None:
            warnings.warn("\'is_admin argument\' is deprecated, use set_group_permissions method instead",
                          DeprecationWarning)

        return self._s.pi_post(f'manage/users/add', data=body)

    def deactivate_user(self, user: [int, str] = None) -> ApiResponse:
        """
        Deactivate a user from its user ID or login. Disabled users can't log in interactively nor user their API keys.
        They do not appear in proposed user lists.

        !!! tip "Requires admin rights"

        Args:
          user: User ID or login to deactivate

        Returns:
          ApiResponse object

        """
        user_id = None
        if isinstance(user, int):
            user_id = user

        elif isinstance(user, str):
            user_lookup_r = self._s.pi_get(f'manage/users/lookup/login/{user}', cid=1)
            if user_lookup_r.is_error():
                return ClientApiError(msg=user_lookup_r.get_msg())

            user_id = user_lookup_r.get_data().get('user_id')

        if user_id is None:
            return ClientApiError(msg="Invalid user ID or login")

        return self._s.pi_get(f'manage/users/deactivate/{user_id}')

    def update_user(self,
                    user: Union[int, str],
                    login: str = None,
                    name: str = None,
                    password: str = None,
                    email: str = None,
                    **kwargs) -> ApiResponse:
        """
        Updates a user. The user can be updated if :
        
        - login is unique
        - email is unique
        - password meets the requirements of IRIS
        
        Only set the parameters that needs to be updated.
        
        !!! tip "Requires admin rights"

        Args:
          user: User ID or login to update
          login: Login of the user
          name: Full name of the user
          password: Password of the user
          email: Email of the user

        Returns:
          ApiResponse

        """

        if kwargs.get('is_admin') is not None:
            warnings.warn("\'is_admin\' argument is deprecated, use set_group_permissions method instead",
                          DeprecationWarning)

        user_req = None
        if isinstance(user, int):
            user_req = self._s.pi_get(f'manage/users/{user}')

        elif isinstance(user, str):
            user_req = self.get_user(login=user)

        if user_req.is_error():
            return ClientApiError(msg=f'Unable to fetch user {user} for update',
                                  error=user_req.get_msg())

        user = user_req.get_data()

        body = {
            "user_login": login,
            "user_name": name if name else user.get('user_name'),
            "user_email": email if email else user.get('user_email'),
            "user_password": password if password else "",
            "cid": 1
        }

        return self._s.pi_post(f'manage/users/update/{user.get("user_id")}', data=body)

    def delete_user(self, user: [int, str], **kwargs) -> ApiResponse:
        """
        Deletes a user based on its login. A user can only be deleted if it does not have any
        activities in IRIS. This is to maintain coherence in the database. The user needs to be
        deactivated first.
        
        !!! tip "Requires administrative rights"

        Args:
          user: Username or user ID of the user to delete

        Returns:
          ApiResponse

        """

        if kwargs.get('login') is not None:
            warnings.warn("\'login\' argument is deprecated, use \'user\' instead",
                          DeprecationWarning)
            user = kwargs.get('login')

        if isinstance(user, int):
            return self.delete_user_by_id(user_id=user)

        if user is None:
            return ClientApiError(msg='Invalid user ID or login')

        user_req = self.get_user(login=user)
        if user_req.is_error():
            return ClientApiError(msg=f'Unable to fetch user {user} for update',
                                  error=user_req.get_msg())

        user = user_req.get_data()

        return self.delete_user_by_id(user_id=user.get('user_id'))

    def delete_user_by_id(self, user_id: int) -> ApiResponse:
        """
        Delete a user based on its ID. A user can only be deleted if it does not have any
        activities in IRIS. This is to maintain coherence in the database.
        
        !!! tip "Requires admin rights"

        Args:
          user_id: UserID of the user to delete

        Returns:
          ApiResponse

        """

        return self._s.pi_post(f'manage/users/delete/{user_id}', cid=1)

    def add_ioc_type(self, name: str, description: str, taxonomy: str = None) -> ApiResponse:
        """
        Add a new IOC Type.
        
        !!! tip "Requires admin rights"

        Args:
          name: Name of the IOC type
          description: Description of the IOC type
          taxonomy: Taxonomy of the IOC Type

        Returns:
          ApiResponse

        """
        body = {
            "type_name": name,
            "type_description": description,
            "type_taxonomy": taxonomy if taxonomy else "",
            "cid": 1
        }
        return self._s.pi_post(f'manage/ioc-types/add', data=body)

    def delete_ioc_type(self, ioc_type_id: int) -> ApiResponse:
        """
        Delete an existing IOC Type by its ID.
        
        !!! tip "Requires admin rights"

        Args:
          ioc_type_id: IOC type to delete

        Returns:
          ApiResponse

        """
        return self._s.pi_post(f'manage/ioc-types/delete/{ioc_type_id}', cid=1)

    def update_ioc_type(self, ioc_type_id: int, name: str = None,
                        description: str = None, taxonomy: str = None) -> ApiResponse:
        """
        Updates an IOC type. `ioc_type_id` needs to be a valid existing IocType ID.
        
        !!! tip "Requires admin rights"

        Args:
          ioc_type_id: IOC type to update
          name: Name of the IOC type
          description: Description of the IOC type
          taxonomy: Taxonomy of the IOC Type

        Returns:
          ApiResponse

        """

        ioc_type = IocTypeHelper(session=self._s)
        ioct_req = ioc_type.get_ioc_type(ioc_type_id=ioc_type_id)
        if ioct_req.is_error():
            return ClientApiError(msg=f'Unable to fetch ioc type #{ioc_type_id} for update',
                                  error=ioct_req.get_msg())

        ioc = ioct_req.get_data()

        body = {
            "type_name": name if name else ioc.get('type_name'),
            "type_description": description if description else ioc.get('type_description'),
            "type_taxonomy": taxonomy if taxonomy else ioc.get('type_taxonomy'),
            "cid": 1
        }
        return self._s.pi_post(f'manage/ioc-types/update/{ioc_type_id}', data=body)

    @deprecated(reason='This method is deprecated in IRIS > v1.4.3', action="error", version="2.0.0")
    def add_asset_type(self, name: str, description: str) -> ApiResponse:
        """
        Add a new Asset Type.
        
        !!! tip "Requires admin rights"

        Args:
          name: Name of the Asset type
          description: Description of the Asset type

        Returns:
          ApiResponse

        """
        body = {
            "asset_name": name,
            "asset_description": description,
            "cid": 1
        }
        return self._s.pi_post(f'manage/asset-type/add', data=body)

    def delete_asset_type(self, asset_type_id: int) -> ApiResponse:
        """
        Delete an existing asset type by its ID.
        
        !!! tip "Requires admin rights"

        Args:
          asset_type_id: Asset type to delete

        Returns:
          ApiResponse

        """
        return self._s.pi_post(f'manage/asset-type/delete/{asset_type_id}')

    @deprecated(reason='This method is deprecated in IRIS > v1.4.3', action="error", version="2.0.0")
    def update_asset_type(self, asset_type_id: int, name: str = None,
                          description: str = None) -> ApiResponse:
        """
        Updates an Asset type. `asset_type_id` needs to be a valid existing AssetType ID.
        
        !!! tip "Requires admin rights"

        Args:
          asset_type_id: Asset type to update
          name: Name of the IOC type
          description: Description of the IOC type

        Returns:
          ApiResponse

        """

        asset_type = AssetTypeHelper(session=self._s)
        sat_req = asset_type.get_asset_type(asset_type_id=asset_type_id)
        if sat_req.is_error():
            return ClientApiError(msg=f'Unable to fetch asset type #{sat_req} for update',
                                  error=sat_req.get_msg())

        ioc = sat_req.get_data()

        body = {
            "asset_name": name if name else ioc.get('asset_name'),
            "asset_description": description if description else ioc.get('asset_description'),
            "cid": 1
        }
        return self._s.pi_post(f'manage/asset-type/update/{asset_type_id}', data=body)

    def add_customer(self, customer_name: str):
        """
        Creates a new customer. A new customer can be added if:
        
        - customer_name is unique
        
        !!! tip "Requires admin rights"
        Args:
          customer_name: Name of the customer to add.

        Returns:
          ApiResponse object

        """
        body = {
            "customer_name": customer_name.lower()
        }
        resp = self._s.pi_post('manage/customers/add',
                               data=body)
        return resp

    def update_customer(self, customer_id: int, customer_name: str):
        """
        Updates an existing customer. A customer can be updated if :
        
        - `customer_id` is a know customer ID in IRIS
        - `customer_name` is unique
        
        !!! tip "Requires admin rights"

        Args:
          customer_id: ID of the customer to update
          customer_name: Customer name

        Returns:
          ApiResponse object

        """
        body = {
            "customer_name": customer_name.lower()
        }
        resp = self._s.pi_post(f'/manage/customers/update/{customer_id}',
                               data=body)
        return resp

    def delete_customer(self, customer: Union[str, int]) -> ApiResponse:
        """
        Deletes a customer from its ID or name.
        
        !!! tip "Requires admin rights"

        Args:
          customer: Customer name or customer ID

        Returns:
          ApiResponse object

        """
        if isinstance(customer, str):

            c = Customer(session=self._s)
            c_id = c.lookup_customer(customer_name=customer)

            if not c_id:
                return ClientApiError(f'Customer {customer} not found')

            data = get_data_from_resp(c_id)
            c_id = parse_api_data(data, 'customer_id')

        else:
            c_id = customer

        resp = self._s.pi_post(f'manage/customers/delete/{c_id}', cid=1)

        return resp

    def add_group(self, group_name: str, group_description: str, group_permissions: List[Permissions]) -> ApiResponse:
        """
        Add a new group with permissions. Cases access and members can be set later on with
        `set_group_access` and `set_group_members` methods. Permissions must be a list of known
        permissions from the Permission enum.

        Args:
            group_name: Name of the group
            group_description: Description of the group
            group_permissions: List of permission from Permission enum

        Returns:
            ApiResponse object
        """
        for perm in group_permissions:
            if not isinstance(perm, Permissions):
                return ClientApiError(msg=f'Invalid permission {perm}')

        body = {
            "group_name": group_name,
            "group_description": group_description,
            "group_permissions": [perm.value for perm in group_permissions],
            "cid": 1
        }

        return self._s.pi_post('manage/groups/add', data=body)

    def delete_group(self, group: Union[str, int]) -> ApiResponse:
        """
        Delete a group by its ID or name.

        Args:
            group: Group ID or group name

        Returns:
            ApiResponse object
        """
        return self._s.pi_post(f'manage/groups/delete/{group}', cid=1)

    def list_groups(self) -> ApiResponse:
        """
        List all groups.

        Returns:
            ApiResponse object
        """
        return self._s.pi_get('manage/groups/list', cid=1)

    def lookup_group(self, group_name: str) -> ApiResponse:
        """
        Lookup a group by its name.

        Args:
            group_name: Group name

        Returns:
            ApiResponse object
        """
        group_lists = self.list_groups()
        if group_lists.is_error():
            return group_lists

        for group in group_lists.get_data():
            if group.get('group_name').lower() == group_name.lower():
                response = ClientApiData(data=group)

                return ApiResponse(response=response, uri=group_lists.get_uri())

        return ClientApiError(msg=f'Group {group_name} not found')

    def set_group_permissions(self, group_id: int = None, permissions: List[Permissions] = None) -> ApiResponse:
        """
        Set the permissions of a group.
        Permissions must be a list of known permissions ID from the Permission enum

        !!! tips "Calling user must have the manage_users permission"

        Args:
            group_id: Group ID to set permissions
            permissions: List of permission from Permission enum

        Returns:
            ApiResponse object
        """
        body = {
            "",
            ""
        }
        return self._s.pi_post(f'manage/groups/{group_id}/permissions', data=body)