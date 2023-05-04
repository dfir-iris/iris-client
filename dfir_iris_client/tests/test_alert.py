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
import datetime
import json
from pathlib import Path

import pytest

from dfir_iris_client.admin import AdminHelper
from dfir_iris_client.alert import Alert
from dfir_iris_client.case import Case
from dfir_iris_client.customer import Customer
from dfir_iris_client.helper.colors import EventWhite
from dfir_iris_client.helper.report_template_types import ReportTemplateType, ReportTemplateLanguage
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data, get_data
from dfir_iris_client.tests.tests_helper import InitIrisClientTest


def load_alert_data():
    """Load alert data from a file"""
    with open(Path(__file__).parent / 'resources' / 'alert.json') as f:
        return json.load(f)


def load_invalid_alert_data():
    """Load invalid alert data from a file"""
    with open(Path(__file__).parent / 'resources' / 'alert.json') as f:
        data = json.load(f)

    data['alert_title'] = None
    del data['alert_description']

    return data


def assert_alert_isvalid(data, alert_id, has_related_alerts=False):
    """Assert that the alert data is valid"""
    assert parse_api_data(data, 'alert_id') == alert_id
    assets = parse_api_data(data, 'assets')

    assert isinstance(assets, list)

    assert isinstance(parse_api_data(data, 'alert_severity_id'), int)
    assert isinstance(parse_api_data(data, 'alert_owner_id'), int) or parse_api_data(data, 'alert_owner_id') is None

    alert_source_content = parse_api_data(data, 'alert_source_content')
    assert isinstance(alert_source_content, dict)

    comments = parse_api_data(data, 'comments')
    assert isinstance(comments, list)

    modification_history = parse_api_data(data, 'modification_history')
    assert isinstance(modification_history, dict)

    customer = parse_api_data(data, 'customer')
    assert isinstance(customer, dict)

    owner = parse_api_data(data, 'owner')
    assert isinstance(owner, dict) or owner is None

    assert isinstance(parse_api_data(data, 'alert_source_link'), str)

    cases = parse_api_data(data, 'cases')
    assert isinstance(cases, list)

    assert isinstance(parse_api_data(data, 'alert_classification_id'), int)
    assert isinstance(parse_api_data(data, 'alert_source'), str)
    assert isinstance(parse_api_data(data, 'alert_tags'), str)
    assert isinstance(parse_api_data(data, 'alert_context'), dict)
    assert isinstance(parse_api_data(data, 'alert_id'), int)

    severity = parse_api_data(data, 'severity')
    assert isinstance(severity, dict)

    alert_creation_time = parse_api_data(data, 'alert_creation_time')
    assert isinstance(alert_creation_time, str)

    classification = parse_api_data(data, 'classification')
    assert isinstance(classification, dict)

    assert isinstance(parse_api_data(data, 'alert_title'), str)
    assert isinstance(parse_api_data(data, 'alert_uuid'), str)
    assert isinstance(parse_api_data(data, 'alert_source_ref'), str)
    assert isinstance(parse_api_data(data, 'alert_note'), str)
    assert isinstance(parse_api_data(data, 'alert_customer_id'), int)

    iocs = parse_api_data(data, 'iocs')
    assert isinstance(iocs, list)

    assert isinstance(parse_api_data(data, 'alert_description'), str)
    assert isinstance(parse_api_data(data, 'alert_status_id'), int)

    alert_source_event_time = parse_api_data(data, 'alert_source_event_time')
    assert isinstance(alert_source_event_time, str)

    status = parse_api_data(data, 'status')
    assert isinstance(status, dict)

    if has_related_alerts:
        related_alerts = parse_api_data(data, 'related_alerts')
        assert isinstance(related_alerts, dict)


class AlertTest(InitIrisClientTest):

    def setUp(self) -> None:
        """ """
        self.alert = Alert(self.session)

    def test_get_alert(self):
        """ """
        resp = self.alert.get_alert(1)

        assert bool(assert_api_resp(resp)) is True
        data = get_data_from_resp(resp)

        assert_alert_isvalid(data,1, has_related_alerts=True)

    def test_get_alerts(self):
        """ """
        resp = self.alert.get_alerts([1, 2, 3, 4, 5, 6])

        assert bool(assert_api_resp(resp)) is True
        data = get_data_from_resp(resp)

        assert isinstance(data, dict)

        for alert in parse_api_data(data, 'alerts'):
            assert_alert_isvalid(alert, parse_api_data(alert, 'alert_id'))

    def test_add_alert(self):
        """ """
        alert_data = load_alert_data()

        resp = self.alert.add_alert(alert_data)
        assert bool(assert_api_resp(resp)) is True

        data = get_data_from_resp(resp)
        assert_alert_isvalid(data, parse_api_data(data, 'alert_id'))

    def test_delete_alert(self):
        """ """
        alert_data = load_alert_data()

        resp = self.alert.add_alert(alert_data)
        assert bool(assert_api_resp(resp)) is True

        data = get_data_from_resp(resp)
        alert_id = parse_api_data(data, 'alert_id')

        resp = self.alert.delete_alert(alert_id)
        assert bool(assert_api_resp(resp)) is True

    def test_update_alert(self):
        """ """
        alert_data = load_alert_data()

        resp = self.alert.add_alert(alert_data)
        assert bool(assert_api_resp(resp)) is True

        data = get_data_from_resp(resp)
        alert_id = parse_api_data(data, 'alert_id')

        resp = self.alert.update_alert(alert_id, {'alert_title': 'test'})
        assert bool(assert_api_resp(resp)) is True

        data = get_data_from_resp(resp)
        assert parse_api_data(data, 'alert_title') == 'test'

    def test_add_alert_failure(self):
        """Test adding an alert with invalid data should fail."""
        alert_data = load_invalid_alert_data()

        resp = self.alert.add_alert(alert_data)
        assert bool(assert_api_resp(resp)) is False

    def test_delete_alert_failure(self):
        """Test deleting a non-existent alert should fail."""
        non_existent_alert_id = -1

        resp = self.alert.delete_alert(non_existent_alert_id)
        assert bool(assert_api_resp(resp)) is False

    def test_update_alert_failure(self):
        """Test updating an alert with invalid data should fail."""
        alert_data = load_alert_data()

        resp = self.alert.add_alert(alert_data)
        assert bool(assert_api_resp(resp)) is True

        alert_id = get_data(resp, 'alert_id')

        invalid_update_data = {'alert_title': None}
        resp = self.alert.update_alert(alert_id, invalid_update_data)
        assert bool(assert_api_resp(resp)) is False

    def test_escalate_alert(self):
        """ Test escalating an alert """
        alert_data = load_alert_data()

        resp = self.alert.add_alert(alert_data)
        assert bool(assert_api_resp(resp)) is True

        alert_id = resp.get_data_field('alert_id')

        iocs = resp.get_data_field('iocs')
        ioc_uid = iocs[0].get('ioc_uid')

        asset = resp.get_data_field('assets')
        asset_uid = asset[0].get('asset_uid')

        resp = self.alert.escalate_alert(alert_id, iocs_import_list=[ioc_uid],
                                         assets_import_list=[asset_uid], escalation_note='test',
                                         case_title='test', case_tags='defender,test', import_as_event=True)

        assert bool(assert_api_resp(resp)) is True

        data = get_data_from_resp(resp)
        assert 'classification_id' in data
        assert 'case_uuid' in data
        assert 'case_name' in data and 'test' in data['case_name']
        assert 'case_id' in data
        assert 'case_customer' in data
        assert 'modification_history' in data
        assert 'case_description' in data
        assert 'case_soc_id' in data
        assert 'status_id' in data

    def test_merge_alert(self):
        """ Test merging an alert """
        alert_data = load_alert_data()

        resp = self.alert.add_alert(alert_data)
        assert bool(assert_api_resp(resp)) is True

        alert_id = resp.get_data_field('alert_id')

        iocs = resp.get_data_field('iocs')
        ioc_uid = iocs[0].get('ioc_uid')

        asset = resp.get_data_field('assets')
        asset_uid = asset[0].get('asset_uid')

        resp = self.alert.merge_alert(alert_id, iocs_import_list=[ioc_uid],
                                      assets_import_list=[asset_uid], merge_note='test',
                                      import_as_event=True, target_case_id=1)

        assert bool(assert_api_resp(resp)) is True

        data = get_data_from_resp(resp)
        assert 'classification_id' in data
        assert 'case_uuid' in data
        assert 'case_name' in data and 'test' in data['case_name']
        assert 'case_id' in data
        assert 'case_customer' in data
        assert 'modification_history' in data
        assert 'case_description' in data
        assert 'case_soc_id' in data
        assert 'status_id' in data