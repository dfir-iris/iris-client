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
from typing import List

import pytest
from dfir_iris_client.helper.authorization import Permissions


class User(object):
    """ """
    def __init__(self, username=None, login=None, password=None, email=None):
        """ """
        self.username = username
        self.login = login
        self.password = password
        self.email = email


class Group(object):
    """ """
    def __init__(self, **kwargs):
        """ """
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.permissions = []
        self.group_auto_follow = kwargs.get('group_auto_follow', False)
        self.group_auto_follow_access_level = kwargs.get('group_auto_follow_access_level', 0)


@pytest.fixture(scope="class")
def standard_user(request):
    """ """
    user = User()
    user.login = 'test_user'
    user.password = 'TestPassword1-'
    user.username = 'test_user'
    user.email = 'test@iris.local'

    request.cls.standard_user = user


@pytest.fixture(scope="class")
def standard_group(request):
    """ """
    group = Group()
    group.name = 'test_group'
    group.description = 'test group description'
    group.permissions = [Permissions.standard_user]

    request.cls.standard_group = group


@pytest.fixture(scope="class")
def admin_group(request):
    """ """
    group = Group()
    group.name = 'test_adm_group'
    group.description = 'test adm group description'
    group.permissions = [Permissions.server_administrator, Permissions.standard_user]

    request.cls.admin_group = group


@pytest.fixture(scope="class")
def native_admin_group(request):
    """ """
    group = Group()
    group.name = 'Administrators'
    group.description = 'Administrators'
    group.permissions = [Permissions.server_administrator, Permissions.standard_user]
    group.group_auto_follow = True
    group.group_auto_follow_access_level = 4

    request.cls.native_admin_group = group
