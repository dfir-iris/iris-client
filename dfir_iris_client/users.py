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

from deprecated.classic import deprecated

from dfir_iris_client.helper.utils import ApiResponse


class User(object):
    """Handles the users type methods"""
    def __init__(self, session):
        self._s = session

    @deprecated('Use the new user_exists method', version="2.0.0", action="error")
    def user_id_exists(self, user_id: int) -> bool:
        return self.user_exists(user=user_id)

    @deprecated('Use the new user_exists method', version="2.0.0", action="error")
    def username_exists(self, username: str) -> bool:
        return self.user_exists(user=username)

    def user_exists(self, user: Union[str, int]) -> bool:
        """
        Returns True if the user (login) exists, else false. User ID can also be looked up.

        Args:
          user: Login or user ID to lookup

        Returns:
          True if exists else false
        """
        if isinstance(user, int):
            req = self.get_user(user_id=user)
        else:
            req = self.lookup_username(username=user)

        return req.is_success()

    def lookup_username(self, username: str) -> ApiResponse:
        """
        Returns a user ID corresponding to the username, else None

        Args:
          username: Username to lookup

        Returns:
          ApiResponse

        """
        return self._s.pi_get(f'manage/users/lookup/login/{username}')

    def get_user(self, user: Union[int, str], **kwargs) -> ApiResponse:
        """Return a user data

        Args:
          user: User ID or login of the user to get

        Returns:
          ApiResponse object
        """
        if kwargs.get('user_id'):
            raise DeprecationWarning('user_id is deprecated, use user instead')

        if isinstance(user, str):
            return self.lookup_username(username=user)

        return self._s.pi_get(f'manage/users/lookup/id/{user}')

    def list_users(self) -> ApiResponse:
        """
        Returns a list of the users with a restricted view so it can be called by unprivileged users.

        Args:

        Returns:
            ApiResponse object
        """
        return self._s.pi_get(f'manage/users/restricted/list')

