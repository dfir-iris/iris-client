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

from dfir_iris_client.helper.alert_status import AlertStatusHelper
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import InitIrisClientTest


class AlertStatusTest(InitIrisClientTest):
    """ """

    def setUp(self) -> None:
        """ """
        self.asset_type = AlertStatusHelper(self.session)

    def test_list_alert_status(self):
        """ """
        ret = self.asset_type.list_alert_status_types()

        assert assert_api_resp(ret)

        assert ret.get_data_field('status_name', index=0) is not None
        assert ret.get_data_field('status_description', index=0) is not None
        assert ret.get_data_field('status_id', index=0) is not None

    def test_get_alert_status_by_id(self):
        """ """
        ret = self.asset_type.list_alert_status_types()

        assert assert_api_resp(ret, soft_fail=False)

        ret = self.asset_type.get_alert_status(ret.get_data_field('status_id', index=0))
        assert assert_api_resp(ret, soft_fail=False)

        assert ret.get_data_field('status_name') is not None
        assert ret.get_data_field('status_description') is not None
        assert ret.get_data_field('status_id') is not None

    def test_get_alert_status_by_name(self):
        """ """
        ret = self.asset_type.list_alert_status_types()

        assert assert_api_resp(ret, soft_fail=False)

        ret = self.asset_type.lookup_alert_status_name(ret.get_data_field('status_name', index=0))
        assert ret is not None
