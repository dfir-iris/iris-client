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
import os

import pytest

from dfir_iris_client.admin import AdminHelper
from dfir_iris_client.helper.authorization import Permissions
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import InitIrisClientTest


@pytest.mark.usefixtures('standard_user', 'standard_group', 'admin_group', 'native_admin_group')
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

    def test_get_user_valid(self):
        """ """
        ret = self.adm.get_user('administrator')
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'user_active') is True
        assert type(parse_api_data(data, 'user_id')) is int
        assert type(parse_api_data(data, 'user_uuid')) is str
        assert parse_api_data(data, 'user_login') == os.getenv('IRIS_ADM_USERNAME', default='administrator')
        assert parse_api_data(data, 'user_name') == os.getenv('IRIS_ADM_USERNAME', default="administrator")
        assert parse_api_data(data, 'user_email') == os.getenv('IRIS_ADM_EMAIL', default="administrator@localhost")
        assert type(parse_api_data(data, 'user_cases_access')) is list
        assert type(parse_api_data(data, 'user_groups')) is list
        assert type(parse_api_data(data, 'user_organisations')) is list
        assert type(parse_api_data(data, 'user_permissions')) is list

    def test_get_user_invalid(self):
        """ """
        ret = self.adm.get_user('dummy user')
        assert bool(assert_api_resp(ret)) is False

        assert 'Invalid login' in ret.get_msg()

    def test_add_group(self):
        """ """
        std_perm = 0
        for perm in self.standard_group.permissions:
            std_perm += perm.value

        ret = self.adm.add_group(group_name=self.standard_group.name,
                                 group_description=self.standard_group.description,
                                 group_permissions=self.standard_group.permissions)

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'group_name') == self.standard_group.name
        assert type(parse_api_data(data, 'group_id')) is int
        assert type(parse_api_data(data, 'group_uuid')) is str
        assert parse_api_data(data, 'group_auto_follow') is False
        assert parse_api_data(data, 'group_permissions') == std_perm

        ret = self.adm.delete_group(parse_api_data(data, 'group_id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_delete_group_invalid(self):
        """ """
        ret = self.adm.delete_group(999999)
        assert bool(assert_api_resp(ret)) is False

        assert 'invalid group id' in ret.get_msg().lower()

    def test_list_groups(self):
        """ """
        ret = self.adm.list_groups()
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert type(parse_api_data(data[0], 'group_auto_follow')) is bool
        assert type(parse_api_data(data[0], 'group_auto_follow_access_level')) is int
        assert type(parse_api_data(data[0], 'group_description')) is str
        assert type(parse_api_data(data[0], 'group_id')) is int
        assert type(parse_api_data(data[0], 'group_members')) is list
        assert type(parse_api_data(data[0], 'group_name')) is str
        assert type(parse_api_data(data[0], 'group_permissions')) is int
        assert type(parse_api_data(data[0], 'group_permissions_list')) is list
        assert type(parse_api_data(data[0], 'group_uuid')) is str

    def test_lookup_group(self):
        """ """
        ret = self.adm.lookup_group(group_name=self.native_admin_group.name)
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)

        adm_perm = 0
        for perm in self.native_admin_group.permissions:
            adm_perm += perm.value

        assert parse_api_data(data, 'group_name').lower() == self.native_admin_group.name.lower()
        assert type(parse_api_data(data, 'group_id')) is int
        assert type(parse_api_data(data, 'group_uuid')) is str
        assert parse_api_data(data, 'group_auto_follow') is self.native_admin_group.group_auto_follow
        assert parse_api_data(data, 'group_permissions') == adm_perm
        assert parse_api_data(data, 'group_auto_follow_access_level') == self.native_admin_group.group_auto_follow_access_level
