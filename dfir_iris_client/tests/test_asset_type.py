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

from dfir_iris_client.helper.assets_type import AssetTypeHelper
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import new_session


class AssetTypeTest(unittest.TestCase):
    def setUp(self):
        session = new_session()
        self.asset_type = AssetTypeHelper(session)

    def test_list_asset_types(self):
        ret = self.asset_type.list_asset_types()

        assert assert_api_resp(ret)

        data = get_data_from_resp(ret)
        assert parse_api_data(data[0], 'asset_description') is not None
        assert parse_api_data(data[0], 'asset_id') is not None
        assert parse_api_data(data[0], 'asset_name') is not None

    def test_get_asset_type_by_id(self):
        ret = self.asset_type.get_asset_type(1)

        assert assert_api_resp(ret)

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'asset_description') is not None
        assert parse_api_data(data, 'asset_id') is not None
        assert parse_api_data(data, 'asset_name') is not None

    def test_get_asset_type_by_name(self):
        ret = self.asset_type.lookup_asset_type_name('Account')

        assert ret is not None