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


class User(object):
    """ """
    def __init__(self, username=None, login=None, password=None, email=None):
        """ """
        self.username = username
        self.login = login
        self.password = password
        self.email = email


@pytest.fixture(autouse=True)
def standard_user():
    """ """
    return User(username='test_user', login='test_user',
                password='Test_User1!!', email="test@iris.local")

