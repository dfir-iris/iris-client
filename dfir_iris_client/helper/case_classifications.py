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


class CaseClassificationsHelper(object):
    """Handles the case classifications methods"""
    def __init__(self, session):
        self._s = session

    def list_case_classifications(self) -> ApiResponse:
        """
        Returns a list of all case classifications

        Args:

        Returns:
            APIResponse object
        """
        return self._s.pi_get('manage/case-classifications/list', cid=1)

    def lookup_case_classification_name(self, case_classification_name: str) -> Union[None, int]:
        """
        Returns a case_classification_name from its name otherwise None

        Args:
          case_classification_name: Case classification name to lookup

        Returns:
          case_classification_name matching provided case classification name otherwise none

        """
        ast_list = self.list_case_classifications()
        if ast_list:
            for ast in ast_list.get_data():
                if ast.get('name').lower() == case_classification_name.lower():
                    return ast.get('id')

        return None

