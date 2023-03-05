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

from dfir_iris_client.helper.case_classifications import CaseClassificationsHelper
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import InitIrisClientTest


class CaseClassificationsTest(InitIrisClientTest):
    """ """
    def setUp(self):
        """ """
        self.ccl = CaseClassificationsHelper(self.session)

    def test_case_classifications(self):
        """ """
        ret = self.ccl.list_case_classifications()

        assert assert_api_resp(ret)

        data = get_data_from_resp(ret)
        assert isinstance(parse_api_data(data[0], 'creation_date'), str)
        assert isinstance(parse_api_data(data[0], 'description'), str)
        assert isinstance(parse_api_data(data[0], 'id'), int)
        assert isinstance(parse_api_data(data[0], 'name'), str)
        assert isinstance(parse_api_data(data[0], 'name_expanded'), str)

    