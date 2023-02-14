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

from dfir_iris_client.customer import Customer
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import new_session, new_adm_session


class CustomerTest(unittest.TestCase):
    """ """
    docker_compose = None
    session = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.session, cls.docker_compose = new_adm_session()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.docker_compose.stop()

    def setUp(self):
        """ """
        self.customers = Customer(self.session)

    def test_list_customers(self):
        """ """
        ret = self.customers.list_customers()

        assert assert_api_resp(ret)

        data = get_data_from_resp(ret)
        assert parse_api_data(data[0], 'customer_id') is not None
        assert parse_api_data(data[0], 'customer_name') is not None

    def test_get_customer_by_id(self):
        """ """
        ret = self.customers.list_customers()

        assert assert_api_resp(ret, soft_fail=False)
        data = get_data_from_resp(ret)

        ret = self.customers.get_customer_by_id(parse_api_data(data[0], 'customer_id'))
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'customer_id') is not None
        assert parse_api_data(data, 'customer_name') is not None

    def test_get_customer_by_name(self):
        """ """
        ret = self.customers.list_customers()

        assert assert_api_resp(ret, soft_fail=False)
        data = get_data_from_resp(ret)

        ret = self.customers.lookup_customer(parse_api_data(data[0], 'customer_name'))
        assert ret is not None