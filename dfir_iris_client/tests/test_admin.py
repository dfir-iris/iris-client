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

import pytest

from dfir_iris_client.admin import AdminHelper
from dfir_iris_client.customer import Customer
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import new_session, new_adm_session


class AdminTest(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        session = new_adm_session()
        self.adm = AdminHelper(session)
        self.customer = Customer(session)

    def test_is_user_admin_valid_deprecated(self):
        """ """
        # Expect method deprecated exception
        with self.assertRaises(DeprecationWarning):
            self.adm.is_user_admin()

    def test_get_user_valid(self):
        """ """
        ret = self.adm.get_user('administrator')
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'user_active') is True
        assert type(parse_api_data(data, 'user_id')) is int
        assert parse_api_data(data, 'user_login') == "administrator"
        assert parse_api_data(data, 'user_name') == "administrator"
        assert type(parse_api_data(data, 'user_roles')) == list

    def test_get_user_invalid(self):
        """ """
        ret = self.adm.get_user('dummy user')
        assert bool(assert_api_resp(ret)) is False

        assert 'Invalid login' in ret.get_msg()

    def test_add_ioc_type_valid(self):
        """ """
        ret = self.adm.add_ioc_type('dummy ioc type', description='dummy description', taxonomy='dummy taxo')
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'type_description') == 'dummy description'
        assert parse_api_data(data, 'type_name') == 'dummy ioc type'
        assert parse_api_data(data, 'type_taxonomy') == 'dummy taxo'
        assert type(parse_api_data(data, 'type_id')) == int

        ret = self.adm.delete_ioc_type(parse_api_data(data, 'type_id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_ioc_type_invalid_already_exists(self):
        """ """
        ret = self.adm.add_ioc_type('AS', description='dummy description', taxonomy='dummy taxo')
        assert bool(assert_api_resp(ret, soft_fail=True)) == False

        assert 'Data error' in ret.get_msg()

    def test_update_ioc_type_valid(self):
        """ """
        ret = self.adm.add_ioc_type('dummy ioc type', description='dummy description', taxonomy='dummy taxo')
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'type_description') == 'dummy description'
        assert parse_api_data(data, 'type_name') == 'dummy ioc type'
        assert parse_api_data(data, 'type_taxonomy') == 'dummy taxo'
        assert type(parse_api_data(data, 'type_id')) == int

        ret = self.adm.update_ioc_type(ioc_type_id=parse_api_data(data, 'type_id'),
                                       name='new dummy', description='new dummy description', taxonomy='new dummy taxo')
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'type_description') == 'new dummy description'
        assert parse_api_data(data, 'type_name') == 'new dummy'
        assert parse_api_data(data, 'type_taxonomy') == 'new dummy taxo'
        assert type(parse_api_data(data, 'type_id')) == int

        ret = self.adm.delete_ioc_type(parse_api_data(data, 'type_id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_asset_type_valid_deprecated(self):
        """ """
        with self.assertRaises(DeprecationWarning):
            self.adm.add_asset_type('dummy asset type', description='dummy description')
        # assert assert_api_resp(ret, soft_fail=False)
        #
        # data = get_data_from_resp(ret)
        # assert parse_api_data(data, 'asset_description') == 'dummy description'
        # assert parse_api_data(data, 'asset_name') == 'dummy asset type'
        # assert type(parse_api_data(data, 'asset_id')) == int
        #
        # ret = self.adm.delete_asset_type(parse_api_data(data, 'asset_id'))
        # assert assert_api_resp(ret, soft_fail=False)

    def test_add_asset_type_invalid_already_exists(self):
        """ """
        with self.assertRaises(DeprecationWarning):
            self.adm.add_asset_type('WAF', description='dummy description')
        # ret = self.adm.add_asset_type('WAF', description='dummy description')
        # assert bool(assert_api_resp(ret, soft_fail=True)) is False
        #
        # assert 'Data error' in ret.get_msg()

    def test_update_asset_type_valid(self):
        """ """
        with self.assertRaises(Warning):
            self.adm.add_asset_type('dummy asset type', description='dummy description')
        # assert assert_api_resp(ret, soft_fail=False)
        #
        # data = get_data_from_resp(ret)
        # assert parse_api_data(data, 'asset_description') == 'dummy description'
        # assert parse_api_data(data, 'asset_name') == 'dummy asset type'
        # assert type(parse_api_data(data, 'asset_id')) == int
        #
        # ret = self.adm.update_asset_type(asset_type_id=parse_api_data(data, 'asset_id'),
        #                                  name='new dummy', description='new dummy description')
        # assert assert_api_resp(ret, soft_fail=False)
        #
        # data = get_data_from_resp(ret)
        # assert parse_api_data(data, 'asset_description') == 'new dummy description'
        # assert parse_api_data(data, 'asset_name') == 'new dummy'
        # assert type(parse_api_data(data, 'asset_id')) == int
        #
        # ret = self.adm.delete_asset_type(parse_api_data(data, 'asset_id'))
        # assert assert_api_resp(ret, soft_fail=False)

    def test_add_customer_valid(self):
        """ """
        ret = self.adm.add_customer('dummy customer')
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'customer_name') == 'dummy customer'
        assert type(parse_api_data(data, 'customer_id')) is int

        ret = self.adm.delete_customer('dummy customer')
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_customer_invalid_customer_exists(self):
        """ """
        ret = self.adm.add_customer('IrisInitialClient')
        assert bool(assert_api_resp(ret)) is False

        assert 'customer_name' in ret.get_data()

    def test_update_customer_valid(self):
        """ """
        ret = self.customer.lookup_customer(customer_name='IrisInitialClient')
        assert assert_api_resp(ret, soft_fail=False)

        customer_id = parse_api_data(ret.get_data(), 'customer_id')

        ret = self.adm.update_customer(customer_id=customer_id, customer_name='IrisInitialClient2')
        assert assert_api_resp(ret, soft_fail=False)

        ret = self.adm.update_customer(customer_id=customer_id, customer_name='IrisInitialClient')
        assert assert_api_resp(ret, soft_fail=False)

    def test_delete_customer_valid(self):
        """ """
        ret = self.adm.add_customer('dummy customer')
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)

        ret = self.adm.delete_customer(customer=parse_api_data(data, 'customer_id'))
        assert assert_api_resp(ret, soft_fail=False)

        ret = self.adm.add_customer('dummy customer')
        assert assert_api_resp(ret, soft_fail=False)

        ret = self.adm.delete_customer(customer='dummy customer')
        assert assert_api_resp(ret, soft_fail=False)

