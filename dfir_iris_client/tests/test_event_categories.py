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

from dfir_iris_client.helper.events_categories import EventCategoryHelper
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import new_session


class EventCategoryTest(unittest.TestCase):
    def setUp(self):
        session = new_session()
        self.ec = EventCategoryHelper(session)

    def test_list_event_categories(self):
        ret = self.ec.list_events_categories()

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data[0], 'id') is not None
        assert parse_api_data(data[0], 'name') is not None

    def test_get_event_category_by_id(self):
        ret = self.ec.list_events_categories()

        assert assert_api_resp(ret, soft_fail=False)
        data = get_data_from_resp(ret)

        ret = self.ec.get_event_category(parse_api_data(data[0], 'id'))
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'id') is not None
        assert parse_api_data(data, 'name') is not None

    def test_get_event_category_by_name(self):
        ret = self.ec.list_events_categories()

        assert assert_api_resp(ret, soft_fail=False)
        data = get_data_from_resp(ret)

        ret = self.ec.lookup_event_category_name(parse_api_data(data[0], 'name'))
        assert ret is not None

