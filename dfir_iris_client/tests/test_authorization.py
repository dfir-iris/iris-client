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
import pytest

from dfir_iris_client.admin import AdminHelper
from dfir_iris_client.helper.authorization import Permissions
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import InitIrisClientTest


@pytest.mark.usefixtures('standard_user')
class AuthorizationTest(InitIrisClientTest):
    """ """
    @classmethod
    def setUpClass(cls) -> None:
        """ """
        super().setUpClass()
        cls.adm = AdminHelper(cls.session)

    def test_has_permission(self):
        """ """
        ret = self.adm.has_permission(Permissions.server_administrator)
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_user(self):
        """ """
        ret = self.adm.add_user(login=self.standard_user.login,
                                name=self.standard_user.username,
                                password=self.standard_user.password,
                                email=self.standard_user.email)
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'active') is True
        assert parse_api_data(data, 'has_deletion_confirmation') is False
        assert parse_api_data(data, 'external_id') is None
        assert parse_api_data(data, 'in_dark_mode') is None
        assert parse_api_data(data, 'user_login') == self.standard_user.login
        assert parse_api_data(data, 'user_name') == self.standard_user.username
        assert parse_api_data(data, 'user_email') == self.standard_user.email
        assert type(parse_api_data(data, 'uuid')) is str
        assert type(parse_api_data(data, 'id')) is int

        ret = self.adm.deactivate_user(self.standard_user.login)
        assert assert_api_resp(ret, soft_fail=False)

        ret = self.adm.delete_user(self.standard_user.login)
        assert assert_api_resp(ret, soft_fail=False)
