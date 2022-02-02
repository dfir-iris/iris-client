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


class TaskStatusHelper(object):
    """
    Handles the analysis status methods
    """
    def __init__(self, session):
        self._s = session

    def list_task_status_types(self) -> ApiResponse:
        """
        Returns a list of all tasks statuses

        :return: APIResponse object
        """
        return self._s.pi_get('manage/task-status/list')

    def lookup_task_status_name(self, task_status_name: str) -> Union[int, None]:
        """
        Returns a task status ID from its name otherwise None

        :param: task_status_name: str : Name to lookup
        :return: [int, None] - task status ID matching provided task status name
        """
        ast_list = self.list_task_status_types()
        if ast_list:
            for ast in ast_list.get_data():
                if ast.get('status_name').lower() == task_status_name.lower():
                    return ast.get('id')

        return None

    def get_task_status(self, task_status_id: int) -> ApiResponse:
        """
        Returns a task status from its ID

        :param: task_status_id: int : ID to fetch
        :return: ApiResponse object
        """

        return self._s.pi_get(f'manage/task-status/{task_status_id}')
    