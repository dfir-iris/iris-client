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


class CompromiseStatusHelper(object):
    """Handles the compromise status methods"""
    def __init__(self, session):
        self._s = session

    def lookup_compromise_status_name(self, compromise_status_name: str) -> Union[int, None]:
        """Returns a compromise status ID from its name otherwise None

        Args:
          compromise_status_name: str:

        Returns:
          Union[int, None] - compromise status ID matching provided analysis status name or None if not found

        """
        cst_list = self.list_compromise_status_types()
        for ast in cst_list.get_data():
            if ast.get('name').lower() == compromise_status_name.lower():
                return ast.get('value')

        return None

    def list_compromise_status_types(self):
        """Returns a list of all compromise statuses"""
        return self._s.pi_get('manage/compromise-status/list')
