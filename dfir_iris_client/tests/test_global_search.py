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

import unittest

from dfir_iris_client.global_search import global_search_ioc, global_search_notes
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import new_session


class GlobalSearchTest(unittest.TestCase):
    def setUp(self):
        self.session = new_session()

    def test_search_ioc(self):
        ret = global_search_ioc(self.session, search_term='%')

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data[0], 'case_name')
        assert parse_api_data(data[0], 'customer_name')
        assert parse_api_data(data[0], 'ioc_description')

    def test_search_notes(self):
        ret = global_search_notes(self.session, search_term='%')

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data[0], 'case_name')
        assert parse_api_data(data[0], 'client_name')
        assert parse_api_data(data[0], 'note_id')
        assert parse_api_data(data[0], 'note_title')