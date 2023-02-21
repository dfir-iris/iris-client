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
from dfir_iris_client.helper.utils import assert_api_resp

from dfir_iris_client.admin import AdminHelper
from dfir_iris_client.tests.tests_helper import InitIrisClientTest
from dfir_iris_client.helper.authorization import Permissions


class AuthorizationTest(InitIrisClientTest):
    """ """

    def setUp(self) -> None:
        self.adm = AdminHelper(self.session)

    def test_has_permission(self):
        """ """
        ret = self.adm.has_permission(Permissions.server_administrator)
        assert assert_api_resp(ret, soft_fail=False)

