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
import logging as logger

log = logger.getLogger(__name__)


class AssetTypeHelper(object):
    """Handles the assets type methods"""
    def __init__(self, session):
        self._s = session

    def list_asset_types(self) -> ApiResponse:
        """Returns a list of all assets types available

        Args:

        Returns:
            APIResponse object
        """
        return self._s.pi_get('manage/asset-type/list')

    def get_asset_type(self, asset_type_id: int) -> ApiResponse:
        """Returns an asset type data from its id

        Args:
          asset_type_id: ID of asset type to fetch

        Returns:
          ApiResponse

        """
        return self._s.pi_get(f'manage/asset-type/{asset_type_id}')

    def lookup_asset_type_name(self, asset_type_name:str) -> Union[int, None]:
        """Returns an asset type ID from its name otherwise None
        
        :raise: Exception if server data is invalid

        Args:
          asset_type_name: Name of the asset type to lookup

        Returns:
           Union[int, None]: Asset type ID matching provided asset type name

        """
        ast_list = self.list_asset_types()
        for ast in ast_list.get_data():
            if ast.get('asset_name') and ast.get('asset_id'):
                if ast.get('asset_name').lower() == asset_type_name.lower():
                    return ast.get('asset_id')
            else:
                log.error('Unexpected server response. asset_name and asset_id not found in data')
                raise Exception('Unexpected server response. asset_name and asset_id not found in data')

        return None