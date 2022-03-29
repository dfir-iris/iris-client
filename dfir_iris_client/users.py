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
from dfir_iris_client.helper.utils import ApiResponse


class User(object):
    """Handles the users type methods"""
    def __init__(self, session):
        self._s = session

    def user_id_exists(self, user_id: int) -> bool:
        """Returns True if the user ID exists, else false

        Args:
          user_id: User ID to verify

        Returns:
          bool - Asset type ID matching provided asset type name

        """
        req = self.get_user(user_id=user_id)

        return req.is_success()

    def username_exists(self, username: str) -> bool:
        """Returns True if the username (login) exists, else false.
        This is equivalent to calling lookup_username() and getting the results.

        Args:
          username: User name (login) to lookup

        Returns:
          True if exists else false

        """
        req = self.lookup_username(username=username)

        return req.is_success()

    def lookup_username(self, username: str) -> ApiResponse:
        """Returns a user ID corresponding to the username, else None

        Args:
          username: User name to lookup

        Returns:
          ApiResponse

        """

        return self._s.pi_get(f'manage/users/lookup/login/{username}')

    def get_user(self, user_id: int) -> ApiResponse:
        """Return a user data

        Args:
          user_id: USer ID to verify

        Returns:
          bool - Asset type ID matching provided asset type name

        """

        return self._s.pi_get(f'manage/users/lookup/id/{user_id}')

    def list_users(self) -> ApiResponse:
        """Returns a list of the users with a restricted view so it can be called by unprivileged users.

        Args:

        Returns:
            ApiResponse object
        """
        return self._s.pi_get(f'manage/users/restricted/list')