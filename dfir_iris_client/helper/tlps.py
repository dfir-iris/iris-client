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


class TlpHelper(object):
    """
    Handles the TLP methods
    """
    def __init__(self, session):
        self._s = session

    def list_tlps(self) -> ApiResponse:
        """
        Returns a list of all tlps available

        :return: ApiResponse object
        """

        return self._s.pi_get('manage/tlp/list')

    def lookup_tlp_name(self, tlp_name: str) -> Union[int, None]:
        """
        Returns a tlp ID from its name otherwise None

        :return: tlp ID matching provided tlp name or None
        """
        tlp_list_req = self.list_tlps()

        if tlp_list_req:
            for tlp in tlp_list_req.get_data():
                if tlp['tlp_name'].lower() == tlp_name.lower():
                    return tlp['tlp_id']

        return None

    def get_tlp(self, tlp_id: int) -> ApiResponse:
        """
        Returns a tlp from its ID

        :param tlp_id: TLP ID to lookup
        :return: ApiResponse object
        """
        return self._s.pi_get(f'manage/tlp/{tlp_id}')