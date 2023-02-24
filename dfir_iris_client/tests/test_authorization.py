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
from dfir_iris_client.users import User
from dfir_iris_client.helper.authorization import Permissions, CaseAccessLevel
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import InitIrisClientTest, create_standard_user, delete_standard_user_auto, \
    create_standard_group, delete_standard_group


@pytest.mark.usefixtures('standard_user', 'standard_group', 'admin_group', 'native_admin_group')
class AuthorizationTest(InitIrisClientTest):
    """ """
    @classmethod
    def setUpClass(cls) -> None:
        """ """
        super().setUpClass()
        cls.adm = AdminHelper(cls.session)
        cls.users = User(cls.session)

    def test_has_permission(self):
        """ """
        ret = self.adm.has_permission(Permissions.server_administrator)
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_user(self):
        """ """
        ret = create_standard_user(self)
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

        delete_standard_user_auto(self)

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

        ret = create_standard_group(self)

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'group_name') == self.standard_group.name
        assert type(parse_api_data(data, 'group_id')) is int
        assert type(parse_api_data(data, 'group_uuid')) is str
        assert parse_api_data(data, 'group_auto_follow') is False
        assert parse_api_data(data, 'group_permissions') == std_perm

        ret = delete_standard_group(self)
        assert assert_api_resp(ret, soft_fail=False)

    def test_delete_group_by_name(self):
        """ """
        std_perm = 0
        for perm in self.standard_group.permissions:
            std_perm += perm.value

        ret = create_standard_group(self)

        assert assert_api_resp(ret, soft_fail=False)

        ret = self.adm.delete_group(self.standard_group.name)
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

    def test_get_group_by_id(self):
        """ """
        ret = self.adm.get_group(1)
        assert assert_api_resp(ret, soft_fail=False)

    def test_get_group_by_name(self):
        """ """
        ret = self.adm.get_group(self.native_admin_group.name)
        assert assert_api_resp(ret, soft_fail=False)

    def test_group_update(self):
        """ """
        ret = create_standard_group(self)

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        group_id = parse_api_data(data, 'group_id')

        ret = self.adm.update_group(group=group_id,
                                    group_name=self.standard_group.name + ' updated',
                                    group_description=self.standard_group.description + ' updated',
                                    group_permissions=self.admin_group.permissions)

        assert assert_api_resp(ret, soft_fail=False)
        data = get_data_from_resp(ret)

        perms = 0
        for perm in self.admin_group.permissions:
            perms += perm.value

        assert parse_api_data(data, 'group_name') == self.standard_group.name + ' updated'
        assert parse_api_data(data, 'group_description') == self.standard_group.description + ' updated'
        assert parse_api_data(data, 'group_permissions') == perms

        delete_standard_group(self)

    def test_set_group_members(self):
        """ """
        ret = create_standard_group(self)
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        group_id = parse_api_data(data, 'group_id')

        ret = self.adm.update_group_members(group=group_id, members=[1])
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'group_name') == self.standard_group.name
        assert parse_api_data(data, 'group_members')[0].get('id') == 1

        delete_standard_group(self)

    def test_update_group_cases_access(self):
        """ """
        ret = create_standard_group(self)
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        group_id = parse_api_data(data, 'group_id')

        ret = self.adm.update_group_cases_access(group=group_id, cases_list=[1],
                                                 access_level=CaseAccessLevel.read_only, auto_follow=False)
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'group_name') == self.standard_group.name
        assert parse_api_data(data, 'group_auto_follow_access_level') == 0
        assert parse_api_data(data, 'group_cases_access')[0].get('case_id') == 1
        assert parse_api_data(data, 'group_cases_access')[0].get('access_level') == CaseAccessLevel.read_only.value
        gca = parse_api_data(data, 'group_cases_access')[0]
        assert gca.get('access_level_list')[0].get('name') == CaseAccessLevel.read_only.name
        assert gca.get('access_level_list')[0].get('value') == CaseAccessLevel.read_only.value

        delete_standard_group(self)

    def test_list_users(self):
        """ """
        ret = self.users.list_users()
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert type(parse_api_data(data[0], 'user_active')) is bool
        assert type(parse_api_data(data[0], 'user_id')) is int
        assert type(parse_api_data(data[0], 'user_name')) is str
        assert type(parse_api_data(data[0], 'user_login')) is str
        assert type(parse_api_data(data[0], 'user_uuid')) is str

    def test_user_id_exists(self):
        """ """
        ret = create_standard_user(self)
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        user_id = parse_api_data(data, 'id')

        assert self.users.user_exists(user_id) is True

        delete_standard_user_auto(self)

    def test_user_id_exists_failure(self):
        """ """
        assert self.users.user_exists(999999999) is False

    def test_user_name_exists(self):
        """ """
        ret = create_standard_user(self)
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        user_name = parse_api_data(data, 'user_name')

        assert self.users.user_exists(user_name) is True

        delete_standard_user_auto(self)

    def test_user_name_exists_failure(self):
        """ """
        assert self.users.user_exists('nonexistent') is False

