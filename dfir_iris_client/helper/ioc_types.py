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


class IocTypeHelper(object):
    """Handles the IOC types methods"""
    def __init__(self, session):
        self._s = session

    def list_ioc_types(self) -> ApiResponse:
        """
        Returns a list of all ioc types

        Args:

        Returns:
            APIResponse object
        """
        return self._s.pi_get('manage/ioc-types/list', cid=1)

    def lookup_ioc_type_name(self, ioc_type_name: str) -> Union[None, int]:
        """
        Returns an ioc_type_name from its name otherwise None

        Args:
          ioc_type_name: IOC type name to lookup

        Returns:
          ioc_type_name matching provided ioc type name otherwise none

        """
        ast_list = self.list_ioc_types()
        if ast_list:
            for ast in ast_list.get_data():
                if ast.get('type_name').lower() == ioc_type_name.lower():
                    return ast.get('type_id')

        return None

    def get_ioc_type(self, ioc_type_id: int) -> ApiResponse:
        """
        Returns an ioc type from its ID

        Args:
          ioc_type_id: Type ID to lookup

        Returns:
          ApiResponse object

        """
        return self._s.pi_get(f'manage/ioc-types/{ioc_type_id}')