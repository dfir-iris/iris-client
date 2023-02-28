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
from pathlib import Path

from dfir_iris_client.admin import AdminHelper
from dfir_iris_client.case import Case
from dfir_iris_client.customer import Customer
from dfir_iris_client.helper.colors import EventWhite
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.tests.tests_helper import InitIrisClientTest


class CaseTest(InitIrisClientTest):
    """ """

    def setUp(self):
        """ """
        self.case = Case(self.session)
        self.ch = Customer(self.session)
        self.case.set_cid(1)

    def test_add_rm_case_with_existing_customer_id(self):
        """ """
        ret = self.case.add_case(case_name='Dummy case', case_description="Dummy description",
                                 case_customer=1, soc_id='dummy', create_customer=False)

        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        case_id = parse_api_data(data, 'case_id')
        assert parse_api_data(data, 'case_id') is not None

        ret = self.case.delete_case(case_id)
        assert bool(assert_api_resp(ret)) is True

    def test_add_rm_case_with_existing_customer_name(self):
        """ """
        ret = self.case.add_case(case_name='Dummy case', case_description="Dummy description",
                                 case_customer="IrisInitialClient", soc_id='dummy', custom_attributes={},
                                 create_customer=False)

        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        case_id = parse_api_data(data, 'case_id')
        assert parse_api_data(data, 'case_id') is not None

        ret = self.case.delete_case(case_id)
        assert bool(assert_api_resp(ret)) is True

    def test_add_case_with_faulty_customer_id(self):
        """ """
        ret = self.case.add_case(case_name='Dummy case', case_description="Dummy description",
                                 case_customer=15551115, soc_id='dummy',  custom_attributes={}, create_customer=False)

        assert bool(assert_api_resp(ret)) is False

    def test_add_case_with_faulty_customer_name(self):
        """ """
        ret = self.case.add_case(case_name='Dummy case', case_description="Dummy description",
                                 case_customer="Dummy dummy 123", soc_id='dummy', custom_attributes={},
                                 create_customer=False)

        assert bool(assert_api_resp(ret)) is False

    def test_add_case_create_customer_name(self):
        """ """
        ret = self.case.add_case(case_name='Dummy case', case_description="Dummy description",
                                 case_customer="Dummy dummy 123",  custom_attributes={"Test":{"Test":"Test"}},
                                 soc_id='dummy', create_customer=True)

        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        case_id = parse_api_data(data, 'case_id')
        assert parse_api_data(data, 'case_id') is not None

        ret = self.case.delete_case(case_id)
        assert bool(assert_api_resp(ret)) is True

        adm = AdminHelper(self.ch._s)
        ret = adm.delete_customer(customer="Dummy dummy 123")
        assert bool(assert_api_resp(ret)) is True

    def test_get_case_by_id(self):
        """ """
        cid = 1
        ret = self.case.get_case(cid=cid)

        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        case_id = parse_api_data(data, 'case_id')
        assert case_id == cid

    def test_case_id_exists(self):
        """ """
        ret = self.case.case_id_exists(cid=1)
        assert ret is True

        ret = self.case.case_id_exists(cid=1111155555511111)
        assert ret is False

    def test_case_trigger_manual_hook_valid(self):
        ret = self.case.trigger_manual_hook('iris_check_module::on_manual_trigger_case',
                                            module_name='iris_check_module',
                                            targets=[1],
                                            target_type='case')

        assert bool(assert_api_resp(ret)) is True

    def test_case_summary(self):
        """ """

        ret = self.case.get_summary()
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        summary = parse_api_data(data, 'case_description')

        ret = self.case.set_summary('Dummy summary')
        assert bool(assert_api_resp(ret)) is True

        ret = self.case.get_summary()
        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'case_description') == "Dummy summary"

        self.case.set_summary(summary)

    def test_list_get_notes_groups(self):
        """ """

        ret = self.case.list_notes_groups()
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        groups = parse_api_data(data, 'groups')
        if len(groups) > 0:
            assert type(parse_api_data(groups[0], 'group_id')) == int
            assert type(parse_api_data(groups[0], 'group_title')) == str
            assert type(parse_api_data(groups[0], 'notes')) == list

    def test_add_update_rm_notes_group(self):
        """ """
        ret = self.case.add_notes_group("Dummy title")
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        group_id = parse_api_data(data, 'group_id')
        assert type(group_id) == int

        ret = self.case.get_notes_group(group_id=group_id)
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        assert parse_api_data(data, 'group_id') == group_id
        assert parse_api_data(data, 'group_title') == "Dummy title"
        assert parse_api_data(data, 'notes') == []

        self.test_list_get_notes_groups()

        ret = self.case.delete_notes_group(group_id)
        assert bool(assert_api_resp(ret)) is True

        ret = self.case.get_notes_group(group_id=group_id)
        assert bool(assert_api_resp(ret)) is False

    def test_add_update_delete_note_valid_group_id(self):
        """ """
        note_title = "Dummy title"
        note_content = "# Dummy content with markdown\n## Very dummy"
        ret = self.case.add_notes_group("Dummy title")
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        group_id = parse_api_data(data, 'group_id')
        assert type(group_id) == int

        ret = self.case.add_note(note_title=note_title, note_content=note_content, custom_attributes={},
                                 group_id=group_id)
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        note_id = parse_api_data(data, 'note_id')
        assert parse_api_data(data, 'note_content') == note_content
        assert parse_api_data(data, 'note_title') == note_title
        assert type(note_id) == int
        assert type(parse_api_data(data, 'note_creationdate')) == str
        assert type(parse_api_data(data, 'note_lastupdate')) == str

        ret = self.case.update_note(note_id=note_id, note_title='New dummy', note_content='New dummy content',
                                    custom_attributes={"Test":{"Test":"Test"}})
        assert bool(assert_api_resp(ret)) is True

        ret = self.case.get_note(note_id=note_id)
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        note_id = parse_api_data(data, 'note_id')
        group_id = parse_api_data(data, 'group_id')
        assert parse_api_data(data, 'note_content') == "New dummy content"
        assert parse_api_data(data, 'note_title') == "New dummy"
        assert type(note_id) == int
        assert type(parse_api_data(data, 'note_creationdate')) == str
        assert type(parse_api_data(data, 'note_lastupdate')) == str
        assert type(group_id) == int
        assert parse_api_data(data, 'group_title') == note_title

        ret = self.case.delete_note(note_id)
        assert bool(assert_api_resp(ret)) is True

        ret = self.case.delete_notes_group(group_id=group_id)
        assert bool(assert_api_resp(ret)) is True

    def test_add_note_invalid_group(self):
        """ """
        note_title = "Dummy title"
        note_content = "# Dummy content with markdown\n## Very dummy"

        ret = self.case.add_note(note_title=note_title, note_content=note_content,
                                 custom_attributes={"Test": {"Test":"Test"}}, group_id=111555411)
        assert bool(assert_api_resp(ret)) is False

    def test_update_note_invalid_id(self):
        """ """
        ret = self.case.update_note(note_id=111555411, note_title="Dummy title",
                                    custom_attributes={"Test": {"Test":"Test"}}, note_content="Dummy content")
        assert bool(assert_api_resp(ret)) is False

    def test_delete_note_invalid_id(self):
        """ """
        ret = self.case.delete_note(note_id=111555411)
        assert bool(assert_api_resp(ret)) is False

    def test_delete_note_invalid_cid(self):
        """ """
        ret = self.case.delete_note(note_id=111555411, cid=111555411)
        assert bool(assert_api_resp(ret)) is False
        message = ret.get_msg()
        assert "permission denied" in message.lower()

    def test_search_notes(self):
        """ """
        ret = self.case.search_notes("%")
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        assert type(data) == list

    def test_list_assets(self):
        """ """
        ret = self.case.list_assets()
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)
        assert type(data) == dict

        for asset in parse_api_data(data, 'assets'):
            assert type(parse_api_data(asset, 'analysis_status')) is str
            assert type(parse_api_data(asset, 'analysis_status_id')) is int
            self.failureException(parse_api_data(asset, 'asset_compromise_status_id'))
            self.failureException(parse_api_data(asset, 'asset_description'))
            self.failureException(parse_api_data(asset, 'asset_ip'))
            self.failureException(parse_api_data(asset, 'asset_tags'))
            self.failureException(parse_api_data(asset, 'ioc_links'))

            assert type(parse_api_data(asset, 'asset_id')) is int
            assert type(parse_api_data(asset, 'asset_name')) is str
            assert type(parse_api_data(asset, 'asset_type')) is str
            assert type(parse_api_data(asset, 'asset_type_id')) is int
            assert type(parse_api_data(asset, 'link')) is list

    def test_add_rm_asset_valid(self):
        """ """
        ret = self.case.add_asset(name='Dummy asset', asset_type='Account', analysis_status='Unspecified',
                                  compromise_status="not compromised", tags=['tag1', 'tag2'], description='dummy desc',
                                  domain='dummy domain', ip='dummy IP', additional_info='dummy info', ioc_links=[],
                                  custom_attributes={})

        assert bool(assert_api_resp(ret)) is True
        data = get_data_from_resp(ret)

        assert type(parse_api_data(data, 'analysis_status_id')) is int
        assert parse_api_data(data, 'asset_compromise_status_id') == 2
        assert parse_api_data(data, 'asset_description') == "dummy desc"
        assert type(parse_api_data(data, 'asset_id')) is int
        assert type(parse_api_data(data, 'user_id')) is int
        assert type(parse_api_data(data, 'date_added')) is str
        assert type(parse_api_data(data, 'date_update')) is str
        assert parse_api_data(data, 'asset_ip') == "dummy IP"
        assert parse_api_data(data, 'asset_name') == "Dummy asset"
        assert parse_api_data(data, 'asset_tags') == "tag1,tag2"
        assert 'custom_attributes' in data
        assert type(parse_api_data(data, 'asset_type_id')) is int

        ret = self.case.delete_asset(parse_api_data(data, 'asset_id'))
        assert bool(assert_api_resp(ret)) is True

    def test_add_rm_asset_partial_valid(self):
        """ """
        ret = self.case.add_asset(name='Dummy asset', asset_type='Account', analysis_status='Unspecified')

        assert bool(assert_api_resp(ret)) is True
        data = get_data_from_resp(ret)

        assert type(parse_api_data(data, 'analysis_status_id')) is int
        assert parse_api_data(data, 'asset_compromise_status_id') is None
        assert parse_api_data(data, 'asset_description') is None
        assert type(parse_api_data(data, 'asset_id')) is int
        assert type(parse_api_data(data, 'user_id')) is int
        assert type(parse_api_data(data, 'date_added')) is str
        assert type(parse_api_data(data, 'date_update')) is str
        assert parse_api_data(data, 'asset_ip') is None
        assert parse_api_data(data, 'asset_name') == "Dummy asset"
        assert parse_api_data(data, 'asset_tags') is None
        assert parse_api_data(data, 'custom_attributes') is None
        assert type(parse_api_data(data, 'asset_type_id')) is int

        ret = self.case.delete_asset(parse_api_data(data, 'asset_id'))
        assert bool(assert_api_resp(ret)) is True

        ret = self.case.delete_asset(parse_api_data(data, 'asset_id'))
        assert bool(assert_api_resp(ret)) is False

    def test_add_asset_partial_invalid_asset_type(self):
        """ """
        ret = self.case.add_asset(name='Dummy asset', asset_type='Dummy Account', analysis_status='Unspecified')

        assert bool(assert_api_resp(ret)) is False
        message = ret.get_msg()
        assert "asset type" in message.lower()

        ret = self.case.add_asset(name='Dummy asset', asset_type=111155551111, analysis_status='Unspecified')

        assert bool(assert_api_resp(ret)) is False
        data = ret.get_data()
        asset_type_id = parse_api_data(data, 'asset_type_id')
        assert "Invalid" in asset_type_id[0]

    def test_add_asset_partial_invalid_analysis_status(self):
        """ """
        ret = self.case.add_asset(name='Dummy asset', asset_type='Account', analysis_status='dummy analysis status')

        assert bool(assert_api_resp(ret)) is False
        message = ret.get_msg()
        assert "analysis status" in message.lower()

        ret = self.case.add_asset(name='Dummy asset', asset_type='Account', analysis_status=111155551111)

        assert bool(assert_api_resp(ret)) is False
        data = ret.get_data()
        asset_type_id = parse_api_data(data, 'analysis_status_id')
        assert "Invalid" in asset_type_id[0]

    def test_get_asset_valid(self):
        """ """
        ret = self.case.add_asset(name='Dummy asset', asset_type='Account', analysis_status='Unspecified')

        assert bool(assert_api_resp(ret)) is True
        data = get_data_from_resp(ret)

        ret = self.case.asset_exists(parse_api_data(data, 'asset_id'))
        assert ret is True

        ret = self.case.get_asset(parse_api_data(data, 'asset_id'))
        assert bool(assert_api_resp(ret)) is True

        data = get_data_from_resp(ret)

        assert type(parse_api_data(data, 'analysis_status_id')) is int
        assert type(parse_api_data(data, 'asset_compromise_status_id')) in [int, type(None)]
        assert parse_api_data(data, 'asset_description') is None
        assert type(parse_api_data(data, 'asset_id')) is int
        assert type(parse_api_data(data, 'user_id')) is int
        assert type(parse_api_data(data, 'date_added')) is str
        assert type(parse_api_data(data, 'date_update')) is str
        assert parse_api_data(data, 'asset_ip') is None
        assert parse_api_data(data, 'asset_name') == "Dummy asset"
        assert parse_api_data(data, 'asset_tags') is None
        assert type(parse_api_data(data, 'asset_type_id')) is int

        ret = self.case.delete_asset(parse_api_data(data, 'asset_id'))
        assert bool(assert_api_resp(ret)) is True

    def test_get_asset_invalid_id(self):
        """ """
        ret = self.case.get_asset(asset_id=111155551111)
        assert bool(assert_api_resp(ret)) is False

        assert 'Invalid asset ID' in ret.get_msg()

    def test_asset_exists_invalid(self):
        """ """
        ret = self.case.asset_exists(asset_id=111155551111)
        assert ret is False

    def test_update_asset_full_valid(self):
        """ """
        ret = self.case.add_asset(name='Dummy asset', asset_type='Account', analysis_status='Unspecified')

        assert bool(assert_api_resp(ret)) is True
        data = get_data_from_resp(ret)

        ret = self.case.update_asset(asset_id=parse_api_data(data, 'asset_id'), name='Dummy asset 1',
                                     asset_type='Account', analysis_status='Unspecified',
                                     compromise_status=1, tags=['tag1', 'tag2'], description='dummy desc',
                                     domain='dummy domain', ip='dummy IP', additional_info='dummy info', ioc_links=[])

        assert bool(assert_api_resp(ret)) is True
        data = get_data_from_resp(ret)

        assert type(parse_api_data(data, 'analysis_status_id')) is int
        assert type(parse_api_data(data, 'asset_compromise_status_id')) is int
        assert parse_api_data(data, 'asset_description') == "dummy desc"
        assert type(parse_api_data(data, 'asset_id')) is int
        assert type(parse_api_data(data, 'user_id')) is int
        assert type(parse_api_data(data, 'date_added')) is str
        assert type(parse_api_data(data, 'date_update')) is str
        assert parse_api_data(data, 'asset_ip') == "dummy IP"
        assert parse_api_data(data, 'asset_name') == "Dummy asset 1"
        assert parse_api_data(data, 'asset_tags') == "tag1,tag2"
        assert type(parse_api_data(data, 'asset_type_id')) is int

        ret = self.case.delete_asset(parse_api_data(data, 'asset_id'))
        assert bool(assert_api_resp(ret)) is True

    def test_update_asset_invalid_asset_id(self):
        """ """
        ret = self.case.update_asset(asset_id=111155551111, name='Dummy asset',
                                     asset_type='Account', analysis_status='Unspecified',
                                     compromise_status=2, tags=['tag1', 'tag2'], description='dummy desc',
                                     domain='dummy domain', ip='dummy IP', additional_info='dummy info', ioc_links=[])
        assert bool(assert_api_resp(ret)) is False

        assert 'Invalid asset ID' in ret.get_msg()

    def test_update_asset_invalid_multi(self, no_sync=False):
        """

        Args:
          no_sync:  (Default value = False)

        Returns:

        """
        ret = self.case.add_asset(name='Dummy asset', asset_type='Account', analysis_status='Unspecified')

        assert bool(assert_api_resp(ret)) is True
        data = get_data_from_resp(ret)

        ret = self.case.update_asset(asset_id=parse_api_data(data, 'asset_id'), name='Dummy asset',
                                     asset_type='dummy account', analysis_status='Unspecified', no_sync=no_sync)

        assert bool(assert_api_resp(ret)) is False
        assert 'Asset type' in ret.get_msg()

        ret = self.case.update_asset(asset_id=parse_api_data(data, 'asset_id'), name='Dummy asset',
                                     asset_type='Account', analysis_status='dummy analysis status', no_sync=no_sync)

        assert bool(assert_api_resp(ret)) is False
        assert 'Analysis status' in ret.get_msg()

        ret = self.case.update_asset(asset_id=parse_api_data(data, 'asset_id'), name='Dummy asset',
                                     asset_type='Account', analysis_status='Unspecified', ioc_links=[111155551111,
                                                                                                     111155551112],
                                     no_sync=no_sync)

        assert bool(assert_api_resp(ret)) is False
        assert 'IOC' in ret.get_msg()

        ret = self.case.delete_asset(parse_api_data(data, 'asset_id'))
        assert bool(assert_api_resp(ret)) is True

    def test_update_asset_invalid_multi_no_sync(self):
        """ """
        self.test_update_asset_invalid_multi(no_sync=True)

    def test_delete_asset_invalid_asset_id(self):
        """ """
        ret = self.case.delete_asset(asset_id=111155551111)

        assert bool(assert_api_resp(ret)) is False
        assert 'Invalid asset ID' in ret.get_msg()

    def test_list_iocs(self):
        """ """
        ret = self.case.list_iocs()

        assert bool(assert_api_resp(ret)) is True
        data = get_data_from_resp(ret)
        assert type(data) == dict

        for ioc in parse_api_data(data, 'ioc'):
            self.failureException(parse_api_data(ioc, 'ioc_description'))
            self.failureException(parse_api_data(ioc, 'ioc_tags'))
            assert type(parse_api_data(ioc, 'ioc_id')) is int
            assert type(parse_api_data(ioc, 'ioc_tlp_id')) is int
            assert type(parse_api_data(ioc, 'tlp_name')) is str
            assert type(parse_api_data(ioc, 'link')) is list
            assert type(parse_api_data(ioc, 'ioc_value')) is str

    def test_get_ioc_invalid(self):
        """ """
        ret = self.case.get_ioc(ioc_id=111155551111)

        assert bool(assert_api_resp(ret)) is False
        assert 'Invalid IOC ID' in ret.get_msg()

    def test_add_ioc_full_valid(self):
        """ """
        ret = self.case.add_ioc(value="dummy ioc", description="dummy description", ioc_type='AS', ioc_tlp='amber',
                                ioc_tags=['tag1', 'tag2'])

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)

        assert parse_api_data(data, 'ioc_description') == "dummy description"
        assert parse_api_data(data, 'ioc_value') == "dummy ioc"
        assert parse_api_data(data, 'ioc_tags') == "tag1,tag2"

        self.failureException(parse_api_data(data, 'ioc_tlp_id'))
        self.failureException(parse_api_data(data, 'ioc_id'))
        self.failureException(parse_api_data(data, 'ioc_type'))
        self.failureException(parse_api_data(data, 'ioc_type_id'))

        ret = self.case.delete_ioc(ioc_id=parse_api_data(data, 'ioc_id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_ioc_partial_valid(self):
        """ """
        ret = self.case.add_ioc(value="dummy ioc", ioc_type='AS', ioc_tlp='amber')

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)

        assert parse_api_data(data, 'ioc_value') == "dummy ioc"

        self.failureException(parse_api_data(data, 'ioc_tlp_id'))
        self.failureException(parse_api_data(data, 'ioc_id'))
        self.failureException(parse_api_data(data, 'ioc_type'))
        self.failureException(parse_api_data(data, 'ioc_type_id'))
        self.failureException(parse_api_data(data, 'ioc_description'))
        self.failureException(parse_api_data(data, 'ioc_tags'))

        ret = self.case.delete_ioc(ioc_id=parse_api_data(data, 'ioc_id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_ioc_partial_invalid_ioc_type(self):
        """ """
        ret = self.case.add_ioc(value="dummy ioc", ioc_type='dummy AS', ioc_tlp='amber')

        assert bool(assert_api_resp(ret)) is False
        assert 'IOC type' in ret.get_msg()

        ret = self.case.add_ioc(value="dummy ioc", ioc_type=111155551111, ioc_tlp='amber')
        assert bool(assert_api_resp(ret)) is False
        data = get_data_from_resp(ret)
        ioc_type = parse_api_data(data, 'ioc_type_id')
        assert 'Invalid ioc type ID' in ioc_type

    def test_add_ioc_partial_invalid_ioc_tlp(self):
        """ """
        ret = self.case.add_ioc(value="dummy ioc", ioc_type='AS', ioc_tlp='dummy amber')

        assert bool(assert_api_resp(ret)) is False
        assert 'TLP' in ret.get_msg()

        ret = self.case.add_ioc(value="dummy ioc", ioc_type='AS', ioc_tlp=111155551111)
        assert bool(assert_api_resp(ret)) is False
        data = get_data_from_resp(ret)
        ioc_type = parse_api_data(data, 'ioc_tlp_id')
        assert 'Invalid TLP ID' in ioc_type[0]

    def test_update_ioc_full_valid(self):
        """ """
        ret = self.case.add_ioc(value="dummy ioc", ioc_type='AS', ioc_tlp='amber')

        assert assert_api_resp(ret, soft_fail=False)
        data = get_data_from_resp(ret)

        ret = self.case.update_ioc(ioc_id=parse_api_data(data, 'ioc_id'),
                                   value="new dummy ioc", description="new dummy description", ioc_type='AS',
                                   ioc_tlp='amber', ioc_tags=['tag1', 'tag2'])

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)

        assert parse_api_data(data, 'ioc_description') == "new dummy description"
        assert parse_api_data(data, 'ioc_value') == "new dummy ioc"
        assert parse_api_data(data, 'ioc_tags') == "tag1,tag2"

        self.failureException(parse_api_data(data, 'ioc_tlp_id'))
        self.failureException(parse_api_data(data, 'ioc_id'))
        self.failureException(parse_api_data(data, 'ioc_type'))
        self.failureException(parse_api_data(data, 'ioc_type_id'))

        ret = self.case.delete_ioc(ioc_id=parse_api_data(data, 'ioc_id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_update_ioc_full_invalid_ioc_type(self):
        """ """
        ret = self.case.add_ioc(value="dummy ioc", ioc_type='AS', ioc_tlp='amber')

        assert assert_api_resp(ret, soft_fail=False)
        data = get_data_from_resp(ret)

        ioc_id = parse_api_data(data, 'ioc_id')

        ret = self.case.update_ioc(ioc_id=ioc_id, ioc_type='dummy AS')

        assert bool(assert_api_resp(ret)) is False
        assert 'IOC type' in ret.get_msg()

        ret = self.case.update_ioc(ioc_id=ioc_id, ioc_type=111155551111)
        assert bool(assert_api_resp(ret)) is False
        data = get_data_from_resp(ret)
        ioc_type = parse_api_data(data, 'ioc_type_id')
        assert 'Invalid ioc type ID' in ioc_type

        ret = self.case.delete_ioc(ioc_id=ioc_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_update_ioc_full_invalid_ioc_tlp(self):
        """ """
        ret = self.case.add_ioc(value="dummy ioc", ioc_type='AS', ioc_tlp='amber')

        assert assert_api_resp(ret, soft_fail=False)
        data = get_data_from_resp(ret)

        ioc_id = parse_api_data(data, 'ioc_id')

        ret = self.case.update_ioc(ioc_id=ioc_id, ioc_tlp='dummy tlp')

        assert bool(assert_api_resp(ret)) is False
        assert 'TLP' in ret.get_msg()

        ret = self.case.update_ioc(ioc_id=ioc_id, ioc_tlp=111155551111)
        assert bool(assert_api_resp(ret)) is False
        data = get_data_from_resp(ret)
        ioc_type = parse_api_data(data, 'ioc_tlp_id')
        assert 'Invalid TLP ID' in ioc_type[0]

        ret = self.case.delete_ioc(ioc_id=ioc_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_delete_ioc_invalid_ioc_id(self):
        """ """
        ret = self.case.delete_ioc(ioc_id=111155551111)

        assert bool(assert_api_resp(ret)) is False
        assert 'Not a valid IOC' in ret.get_msg()

    def test_list_events_no_filters(self, filter_str=None):
        """

        Args:
          filter:  (Default value = 0)

        Returns:

        """
        filter_str = {} if filter_str is None else filter_str
        ret = self.case.filter_events(filter_str=filter_str)

        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert type(data) == dict

        for event in parse_api_data(data, 'timeline'):
            self.failureException(parse_api_data(event, 'assets'))
            self.failureException(parse_api_data(event, 'iocs'))
            self.failureException(parse_api_data(event, 'category_name'))
            self.failureException(parse_api_data(event, 'event_color'))

            assert type(parse_api_data(event, 'category_name')) is str
            assert type(parse_api_data(event, 'event_content')) is str
            assert type(parse_api_data(event, 'event_date')) is str
            assert type(parse_api_data(event, 'event_date_wtz')) is str
            assert type(parse_api_data(event, 'event_id')) is int
            assert type(parse_api_data(event, 'event_in_graph')) is bool
            assert type(parse_api_data(event, 'event_in_summary')) is bool
            assert type(parse_api_data(event, 'event_tags')) is str
            assert type(parse_api_data(event, 'event_tz')) is str

    def test_list_events_filter_asset(self):
        """ """
        self.test_list_events_no_filters({"tag":["%"]})

    def test_list_events_filter_asset_invalid(self):
        """ """
        self.test_list_events_no_filters({"tag": ["randomrandomrandom"]})

    def test_add_event_full_valid(self):
        """ """
        ret = self.case.add_event(title='dummy event', date_time=datetime.datetime.now(), content='dummy content',
                                  raw_content='dummy raw content', source='dummy source', linked_assets=[],
                                  category='Execution', color=EventWhite, display_in_graph=False,
                                  display_in_summary=True, tags=['tag1', 'tag2'], timezone_string="+01:00")

        assert assert_api_resp(ret, soft_fail=False)
        event = get_data_from_resp(ret)
        assert type(event) == dict

        assert type(parse_api_data(event, 'event_category_id')) is int
        assert parse_api_data(event, 'event_content') == 'dummy content'
        assert parse_api_data(event, 'event_title') == 'dummy event'
        assert parse_api_data(event, 'event_raw') == 'dummy raw content'
        assert parse_api_data(event, 'event_tags') == 'tag1,tag2'
        assert parse_api_data(event, 'event_in_summary') is True
        assert parse_api_data(event, 'event_in_graph') is False
        assert parse_api_data(event, 'event_color') == EventWhite
        assert type(parse_api_data(event, 'event_date')) is str
        assert type(parse_api_data(event, 'event_date_wtz')) is str
        assert type(parse_api_data(event, 'event_id')) is int
        assert type(parse_api_data(event, 'event_tz')) is str

        ret = self.case.delete_event(event_id=parse_api_data(event, 'event_id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_event_partial_valid(self):
        """ """
        ret = self.case.add_event(title='dummy event', date_time=datetime.datetime.now())

        assert assert_api_resp(ret, soft_fail=False)
        event = get_data_from_resp(ret)
        assert type(event) == dict

        self.failureException(parse_api_data(event, 'event_color'))

        assert type(parse_api_data(event, 'event_category_id')) is int
        assert type(parse_api_data(event, 'event_id')) is int
        assert parse_api_data(event, 'event_title') == 'dummy event'

        assert type(parse_api_data(event, 'event_category_id')) is int
        assert type(parse_api_data(event, 'event_content')) is str
        assert type(parse_api_data(event, 'event_date')) is str
        assert type(parse_api_data(event, 'event_date_wtz')) is str
        assert type(parse_api_data(event, 'event_in_graph')) is bool
        assert type(parse_api_data(event, 'event_in_summary')) is bool
        assert type(parse_api_data(event, 'event_tags')) is str
        assert type(parse_api_data(event, 'event_tz')) is str

        ret = self.case.delete_event(event_id=parse_api_data(event, 'event_id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_event_invalid_date(self):
        """ """
        ret = self.case.add_event(title='dummy event', date_time="not a date")

        assert bool(assert_api_resp(ret)) is False
        assert 'Expected datetime' in ret.get_msg()

    def test_add_event_invalid_category(self):
        """ """
        ret = self.case.add_event(title='dummy event', date_time=datetime.datetime.now(), category='dummy cat')

        assert bool(assert_api_resp(ret)) is False
        assert 'Event category' in ret.get_msg()

        ret = self.case.add_event(title='dummy event', date_time=datetime.datetime.now(), category=111155551111)

        assert bool(assert_api_resp(ret)) is False
        data = get_data_from_resp(ret)
        cat = parse_api_data(data, 'event_category_id')
        assert 'Invalid event category' in cat[0]

    def test_update_event_valid(self):
        """ """
        ret = self.case.add_event(title='dummy event', date_time=datetime.datetime.now())

        assert assert_api_resp(ret, soft_fail=False)
        event = get_data_from_resp(ret)
        event_id = parse_api_data(event, 'event_id')

        ret = self.case.update_event(event_id=event_id)
        assert assert_api_resp(ret, soft_fail=False)

        ret = self.case.update_event(event_id=event_id, title="new dummy title", date_time=datetime.datetime.now(),
                                     content='dummy content', raw_content='dummy raw content',
                                     source='dummy source', linked_assets=[], category='Execution',
                                     color=EventWhite, display_in_graph=False, display_in_summary=True,
                                     tags=['tag1', 'tag2'], timezone_string="+01:00")

        assert assert_api_resp(ret, soft_fail=False)
        event = get_data_from_resp(ret)

        assert type(parse_api_data(event, 'event_category_id')) is int
        assert parse_api_data(event, 'event_content') == 'dummy content'
        assert parse_api_data(event, 'event_title') == 'new dummy title'
        assert parse_api_data(event, 'event_raw') == 'dummy raw content'
        assert parse_api_data(event, 'event_tags') == 'tag1,tag2'
        assert parse_api_data(event, 'event_in_summary') is True
        assert parse_api_data(event, 'event_in_graph') is False
        assert parse_api_data(event, 'event_color') == EventWhite
        assert type(parse_api_data(event, 'event_date')) is str
        assert type(parse_api_data(event, 'event_date_wtz')) is str
        assert type(parse_api_data(event, 'event_id')) is int
        assert type(parse_api_data(event, 'event_tz')) is str

        ret = self.case.delete_event(event_id=event_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_update_event_invalid_event_id(self):
        """ """
        ret = self.case.update_event(event_id=111155551111)
        assert bool(assert_api_resp(ret)) is False

        assert "Invalid event ID" in ret.get_msg()

    def test_update_event_invalid_event_cat(self):
        """ """
        ret = self.case.add_event(title='dummy event', date_time=datetime.datetime.now())
        assert assert_api_resp(ret, soft_fail=False)

        event = get_data_from_resp(ret)
        event_id = parse_api_data(event, 'event_id')

        ret = self.case.update_event(event_id=event_id, category='dummy cat')
        assert bool(assert_api_resp(ret)) is False

        assert "Event category" in ret.get_msg()

        ret = self.case.delete_event(event_id=event_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_update_event_invalid_event_date(self):
        """ """
        ret = self.case.add_event(title='dummy event', date_time=datetime.datetime.now())
        assert assert_api_resp(ret, soft_fail=False)

        event = get_data_from_resp(ret)
        event_id = parse_api_data(event, 'event_id')

        ret = self.case.update_event(event_id=event_id, date_time='not a date')
        assert bool(assert_api_resp(ret)) is False

        assert "Expected datetime object" in ret.get_msg()

        ret = self.case.delete_event(event_id=event_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_delete_event_invalid_event_id(self):
        """ """
        ret = self.case.delete_event(event_id=111155551111)
        assert bool(assert_api_resp(ret)) is False

        assert 'Not a valid event ID' in ret.get_msg()

    def test_list_tasks(self):
        """ """
        ret = self.case.list_tasks()
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert type(data) == dict

        for task in parse_api_data(data, 'tasks'):
            assert type(parse_api_data(task, 'task_assignees')) is list
            assert type(parse_api_data(task, 'status_bscolor')) is str
            assert type(parse_api_data(task, 'status_name')) is str
            assert type(parse_api_data(task, 'task_description')) is str
            assert type(parse_api_data(task, 'task_id')) is int
            assert type(parse_api_data(task, 'task_open_date')) is str
            assert type(parse_api_data(task, 'task_tags')) is str
            assert type(parse_api_data(task, 'task_title')) is str
            assert type(parse_api_data(task, 'task_status_id')) is int

    def test_add_task_valid(self):
        """ """
        ret = self.case.add_task(title="dummy title", status='To do', description='dummy description',
                                 assignees=['administrator'], tags=['tag1', 'tag2'])
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        assert type(task) == dict

        assert type(parse_api_data(task, 'id')) is int
        assert type(parse_api_data(task, 'task_case_id')) is int
        assert parse_api_data(task, 'task_close_date') is None
        assert parse_api_data(task, 'task_description') == 'dummy description'
        assert type(parse_api_data(task, 'task_last_update')) is str
        assert type(parse_api_data(task, 'task_open_date')) is str
        assert type(parse_api_data(task, 'task_status_id')) is int
        assert parse_api_data(task, 'task_tags') == 'tag1,tag2'
        assert parse_api_data(task, 'task_title') == "dummy title"
        assert parse_api_data(task, 'task_userid_close') is None
        assert type(parse_api_data(task, 'task_userid_open')) is int
        assert type(parse_api_data(task, 'task_userid_update')) is int

        ret = self.case.delete_task(task_id=parse_api_data(task, 'id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_task_partial_valid(self):
        """ """
        ret = self.case.add_task(title="dummy title", status='To do', assignees=['administrator'])
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        assert type(task) == dict

        assert type(parse_api_data(task, 'id')) is int
        assert type(parse_api_data(task, 'task_case_id')) is int
        assert parse_api_data(task, 'task_close_date') is None
        assert parse_api_data(task, 'task_description') == ""
        assert type(parse_api_data(task, 'task_last_update')) is str
        assert type(parse_api_data(task, 'task_open_date')) is str
        assert type(parse_api_data(task, 'task_status_id')) is int
        assert parse_api_data(task, 'task_tags') == ''
        assert parse_api_data(task, 'task_title') == "dummy title"
        assert parse_api_data(task, 'task_userid_close') is None
        assert type(parse_api_data(task, 'task_userid_open')) is int
        assert type(parse_api_data(task, 'task_userid_update')) is int

        ret = self.case.delete_task(task_id=parse_api_data(task, 'id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_task_partial_invalid_status(self):
        """ """
        ret = self.case.add_task(title="dummy title", status='dummy status', assignees=['administrator'])
        assert bool(assert_api_resp(ret)) is False

        assert "Invalid task status" in ret.get_msg()

        ret = self.case.add_task(title="dummy title", status=111155551111, assignees=['administrator'])
        assert bool(assert_api_resp(ret)) is False

    def test_add_task_partial_invalid_assignee(self):
        """ """
        # Invalid as a string returns an error since it is looked up
        ret = self.case.add_task(title="dummy title", status='To do', assignees=['dummy user'])
        assert bool(assert_api_resp(ret)) is False

        assert "Invalid login" in ret.get_msg()

        # Invalid assignee as an ID does not return an error, the task is just created without assignee
        ret = self.case.add_task(title="dummy title", status='To do', assignees=[111155551111])
        assert bool(assert_api_resp(ret)) is True

    def test_update_task_full(self):
        """ """
        ret = self.case.add_task(title="dummy title", status='To do', assignees=['administrator'])
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        task_id = parse_api_data(task, 'id')

        ret = self.case.update_task(task_id=task_id)
        assert assert_api_resp(ret, soft_fail=False)

        ret = self.case.update_task(task_id=task_id, title="new dummy title", status='Done',
                                    assignees=['administrator'],
                                    description='dummy description', tags=['tag1', 'tag2'])
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        assert type(task) == dict

        assert parse_api_data(task, 'id') == task_id
        assert type(parse_api_data(task, 'task_case_id')) is int
        assert parse_api_data(task, 'task_close_date') is None
        assert parse_api_data(task, 'task_description') == 'dummy description'
        assert type(parse_api_data(task, 'task_last_update')) is str
        assert type(parse_api_data(task, 'task_open_date')) is str
        assert type(parse_api_data(task, 'task_status_id')) is int
        assert parse_api_data(task, 'task_tags') == 'tag1,tag2'
        assert parse_api_data(task, 'task_title') == "new dummy title"
        assert parse_api_data(task, 'task_userid_close') is None
        assert type(parse_api_data(task, 'task_userid_open')) is int
        assert type(parse_api_data(task, 'task_userid_update')) is int

        ret = self.case.delete_task(task_id=task_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_update_task_invalid_status(self):
        """ """
        ret = self.case.add_task(title="dummy title", status='To do', assignees=['administrator'])
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        task_id = parse_api_data(task, 'id')

        ret = self.case.update_task(task_id=task_id, status='dummy status')
        assert bool(assert_api_resp(ret)) is False
        assert "Invalid task status" in ret.get_msg()

        ret = self.case.update_task(task_id=task_id, title="dummy title", status=111155551111)
        assert bool(assert_api_resp(ret)) is False

        ret = self.case.delete_task(task_id=task_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_update_task_invalid_assignee(self):
        """ """
        ret = self.case.add_task(title="dummy title", status='To do', assignees=['administrator'])
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        task_id = parse_api_data(task, 'id')

        ret = self.case.update_task(task_id=task_id, assignees=['dummy assignee'])
        assert bool(assert_api_resp(ret)) is False
        assert "Invalid login" in ret.get_msg()

        ret = self.case.update_task(task_id=task_id, title="dummy title", assignees=[111155551111])
        assert bool(assert_api_resp(ret)) is True

        ret = self.case.delete_task(task_id=task_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_delete_task_invalid(self):
        """ """
        ret = self.case.delete_task(task_id=111155551111)
        assert bool(assert_api_resp(ret)) is False

    def test_list_gtasks(self):
        """ """
        ret = self.case.list_global_tasks()
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert type(data) == dict

        for task in parse_api_data(data, 'tasks'):
            assert type(parse_api_data(task, 'user_name')) is str
            assert type(parse_api_data(task, 'status_bscolor')) is str
            assert type(parse_api_data(task, 'status_name')) is str
            assert type(parse_api_data(task, 'task_assignee_id')) is int
            assert type(parse_api_data(task, 'task_description')) is str
            assert type(parse_api_data(task, 'task_id')) is int
            assert type(parse_api_data(task, 'task_tags')) is str
            assert type(parse_api_data(task, 'task_title')) is str
            assert type(parse_api_data(task, 'task_status_id')) is int

    def test_add_gtask_valid(self):
        """ """
        ret = self.case.add_global_task(title="dummy title", status='To do', description='dummy description',
                                        assignee='administrator', tags=['tag1', 'tag2'])
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        assert type(task) == dict

        assert type(parse_api_data(task, 'task_assignee_id')) is int
        assert type(parse_api_data(task, 'task_id')) is int
        assert parse_api_data(task, 'task_close_date') is None
        assert parse_api_data(task, 'task_description') == 'dummy description'
        assert type(parse_api_data(task, 'task_last_update')) is str
        assert type(parse_api_data(task, 'task_open_date')) is str
        assert type(parse_api_data(task, 'task_status_id')) is int
        assert parse_api_data(task, 'task_tags') == 'tag1,tag2'
        assert parse_api_data(task, 'task_title') == "dummy title"
        assert parse_api_data(task, 'task_userid_close') is None
        self.failureException(parse_api_data(task, 'task_userid_open'))
        assert type(parse_api_data(task, 'task_userid_update')) is int

        ret = self.case.delete_global_task(task_id=parse_api_data(task, 'task_id'))

    def test_add_gtask_partial_valid(self):
        """ """
        ret = self.case.add_global_task(title="dummy title", status='To do', assignee='administrator')
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        assert type(task) == dict

        assert type(parse_api_data(task, 'task_assignee_id')) is int
        assert type(parse_api_data(task, 'task_id')) is int
        assert parse_api_data(task, 'task_close_date') is None
        self.failureException(parse_api_data(task, 'task_description'))
        assert type(parse_api_data(task, 'task_last_update')) is str
        assert type(parse_api_data(task, 'task_open_date')) is str
        assert type(parse_api_data(task, 'task_status_id')) is int
        self.failureException(parse_api_data(task, 'task_tags'))
        assert parse_api_data(task, 'task_title') == "dummy title"
        assert parse_api_data(task, 'task_userid_close') is None
        self.failureException(parse_api_data(task, 'task_userid_open'))
        assert type(parse_api_data(task, 'task_userid_update')) is int

        ret = self.case.delete_global_task(task_id=parse_api_data(task, 'task_id'))

    def test_add_gtask_partial_invalid_status(self):
        """ """
        ret = self.case.add_global_task(title="dummy title", status='dummy status', assignee='administrator')
        assert bool(assert_api_resp(ret)) is False

        assert "Invalid task status" in ret.get_msg()

        ret = self.case.add_global_task(title="dummy title", status=111155551111, assignee='administrator')
        assert bool(assert_api_resp(ret)) is False

    def test_add_gtask_partial_invalid_assignee(self):
        """ """
        ret = self.case.add_global_task(title="dummy title", status='To do', assignee='dummy user')
        assert bool(assert_api_resp(ret)) is False

        assert "Invalid login" in ret.get_msg()

        ret = self.case.add_global_task(title="dummy title", status='To do', assignee=111155551111)
        assert bool(assert_api_resp(ret)) is False

    def test_update_gtask_full(self):
        """ """
        ret = self.case.add_global_task(title="dummy title", status='To do', assignee='administrator')
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        task_id = parse_api_data(task, 'task_id')

        ret = self.case.update_global_task(task_id=task_id)
        assert assert_api_resp(ret, soft_fail=False)

        ret = self.case.update_global_task(task_id=task_id, title="new dummy title", status='Done',
                                           assignee='administrator',
                                           description='dummy description', tags=['tag1', 'tag2'])
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        assert type(task) == dict

        assert type(parse_api_data(task, 'task_assignee_id')) is int
        assert type(parse_api_data(task, 'task_id')) is int
        assert parse_api_data(task, 'task_close_date') is None
        self.failureException(parse_api_data(task, 'task_description'))
        assert type(parse_api_data(task, 'task_last_update')) is str
        assert type(parse_api_data(task, 'task_open_date')) is str
        assert type(parse_api_data(task, 'task_status_id')) is int
        assert parse_api_data(task, 'task_tags') == 'tag1,tag2'
        assert parse_api_data(task, 'task_title') == "new dummy title"
        assert parse_api_data(task, 'task_userid_close') is None
        self.failureException(parse_api_data(task, 'task_userid_open'))
        assert type(parse_api_data(task, 'task_userid_update')) is int

        ret = self.case.delete_global_task(task_id=task_id)
        if ret.is_error():
            print(ret.get_msg())
            print(ret.get_data())
            print(ret.as_json())
            print(ret.get_uri())
            print(task_id)

        assert assert_api_resp(ret, soft_fail=False)

    def test_update_gtask_invalid_status(self):
        """ """
        ret = self.case.add_global_task(title="dummy title", status='To do', assignee='administrator')
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        task_id = parse_api_data(task, 'task_id')

        ret = self.case.update_global_task(task_id=task_id, status='dummy status')
        assert bool(assert_api_resp(ret)) is False
        assert "Invalid task status" in ret.get_msg()

        ret = self.case.update_global_task(task_id=task_id, title="dummy title", status=111155551111)
        assert bool(assert_api_resp(ret)) is False

        ret = self.case.delete_global_task(task_id=task_id)

    def test_update_gtask_invalid_assignee(self):
        """ """
        ret = self.case.add_global_task(title="dummy title", status='To do', assignee='administrator')
        assert assert_api_resp(ret, soft_fail=False)

        task = get_data_from_resp(ret)
        task_id = parse_api_data(task, 'task_id')

        ret = self.case.update_global_task(task_id=task_id, assignee='dummy assignee')
        assert bool(assert_api_resp(ret)) is False
        assert "Invalid login" in ret.get_msg()

        ret = self.case.update_global_task(task_id=task_id, title="dummy title", assignee=111155551111)
        assert bool(assert_api_resp(ret)) is False

        ret = self.case.delete_global_task(task_id=task_id)

    def test_delete_gtask_invalid(self):
        """ """
        ret = self.case.delete_global_task(task_id=111155551111)
        assert bool(assert_api_resp(ret)) is False

    def test_list_evidences(self):
        """ """
        ret = self.case.list_evidences()
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert type(data) == dict

        for evidence in parse_api_data(data, 'evidences'):

            assert type(parse_api_data(evidence, 'date_added')) is str
            self.failureException(parse_api_data(evidence, 'file_description'))
            self.failureException(parse_api_data(evidence, 'file_hash'))
            assert type(parse_api_data(evidence, 'filename')) is str
            assert type(parse_api_data(evidence, 'file_size')) is int
            assert type(parse_api_data(evidence, 'id')) is int
            assert type(parse_api_data(evidence, 'username')) is str

    def test_add_evidence_full_valid(self):
        """ """
        ret = self.case.add_evidence(filename="dummy evidence", file_size=478, description="dummy description",
                                     file_hash="dummy hash")
        assert assert_api_resp(ret, soft_fail=False)

        evidence = get_data_from_resp(ret)
        assert type(parse_api_data(evidence, 'date_added')) is str
        assert parse_api_data(evidence, 'file_description') == 'dummy description'
        assert parse_api_data(evidence, 'file_hash') == 'dummy hash'
        assert parse_api_data(evidence, 'filename') == 'dummy evidence'
        assert parse_api_data(evidence, 'file_size') == 478
        assert type(parse_api_data(evidence, 'id')) is int

        ret = self.case.delete_evidence(parse_api_data(evidence, 'id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_evidence_partial_valid(self):
        """ """
        ret = self.case.add_evidence(filename="dummy evidence", file_size=478)
        assert assert_api_resp(ret, soft_fail=False)

        evidence = get_data_from_resp(ret)
        assert type(parse_api_data(evidence, 'date_added')) is str
        self.failureException(parse_api_data(evidence, 'file_description'))
        self.failureException(parse_api_data(evidence, 'file_hash'))
        assert parse_api_data(evidence, 'filename') == 'dummy evidence'
        assert parse_api_data(evidence, 'file_size') == 478
        assert type(parse_api_data(evidence, 'id')) is int

        ret = self.case.delete_evidence(parse_api_data(evidence, 'id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_add_evidence_partial_invalid_size(self):
        """ """
        ret = self.case.add_evidence(filename="dummy evidence", file_size="dummy_size")
        assert assert_api_resp(ret).is_success() is False

    def test_update_evidence_valid(self):
        """ """
        ret = self.case.add_evidence(filename="dummy evidence", file_size=478)
        assert assert_api_resp(ret, soft_fail=False)

        evidence = get_data_from_resp(ret)
        evidence_id = parse_api_data(evidence, 'id')

        ret = self.case.update_evidence(evidence_id=evidence_id, filename='new dummy evidence',
                                        description='dummy description', file_size=30, file_hash='dummy hash')

        evidence = get_data_from_resp(ret)

        assert type(parse_api_data(evidence, 'date_added')) is str
        assert parse_api_data(evidence, 'file_description') == 'dummy description'
        assert parse_api_data(evidence, 'file_hash') == 'dummy hash'
        assert parse_api_data(evidence, 'filename') == 'new dummy evidence'
        assert parse_api_data(evidence, 'file_size') == 30

        ret = self.case.delete_evidence(evidence_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_update_evidence_invalid_size(self):
        """ """
        ret = self.case.add_evidence(filename="dummy evidence", file_size=478)
        assert assert_api_resp(ret, soft_fail=False)

        evidence = get_data_from_resp(ret)
        evidence_id = parse_api_data(evidence, 'id')

        ret = self.case.update_evidence(evidence_id=evidence_id, file_size="dummy size")
        assert assert_api_resp(ret).is_success() is False

        ret = self.case.delete_evidence(evidence_id)
        assert assert_api_resp(ret, soft_fail=False)

    def test_delete_evidence_invalid_id(self):
        """ """
        ret = self.case.delete_evidence(evidence_id=111155551111)
        assert assert_api_resp(ret).is_success() is False

    def test_list_ds_tree(self):
        """ """
        ret = self.case.list_ds_tree()
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert type(data) == dict

        ds_root = parse_api_data(data, 'd-1')
        assert ds_root.get('is_root') is True
        assert ds_root.get('type') == 'directory'
        assert type(ds_root.get('children')) == dict
        assert type(ds_root.get('name')) == str

    def test_add_ds_file(self):
        """ """
        with open(Path(__file__), 'rb') as fin:
            file_data = fin.read()
            file_size = len(file_data)

        ret = self.case.list_ds_tree()
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert type(data) == dict
        ds_root = next(iter(data)).replace('d-', '')

        ret = self.case.add_ds_file(filename="dummy file", file_stream=open(Path(__file__), 'rb'),
                                    file_description="dummy description", file_is_evidence=True, file_is_ioc=True,
                                    parent_id=ds_root, cid=1)

        assert assert_api_resp(ret, soft_fail=False)

        ds_file = get_data_from_resp(ret)
        assert type(parse_api_data(ds_file, 'file_date_added')) is str
        assert parse_api_data(ds_file, 'file_description') == 'dummy description'
        assert type(parse_api_data(ds_file, 'file_sha256')) is str
        assert type(parse_api_data(ds_file, 'file_uuid')) is str
        assert parse_api_data(ds_file, 'file_original_name') == 'dummy file'
        assert parse_api_data(ds_file, 'file_size') == file_size
        assert parse_api_data(ds_file, 'file_case_id') == 1
        assert parse_api_data(ds_file, 'file_parent_id') == int(ds_root)
        assert parse_api_data(ds_file, 'file_is_evidence') is True
        assert parse_api_data(ds_file, 'file_is_ioc') is True

        ret = self.case.delete_ds_file(parse_api_data(ds_file, 'file_id'))
        assert assert_api_resp(ret, soft_fail=False)

    def test_download_ds_file(self):
        """ """
        with open(Path(__file__), 'rb') as fin:
            file_data = fin.read()
            file_size = len(file_data)

        ret = self.case.list_ds_tree()
        assert assert_api_resp(ret, soft_fail=False)

        data = get_data_from_resp(ret)
        assert type(data) == dict
        ds_root = next(iter(data)).replace('d-', '')

        ret = self.case.add_ds_file(filename="dummy file", file_stream=open(Path(__file__), 'rb'),
                                    file_description="dummy description", file_is_evidence=False, file_is_ioc=False,
                                    parent_id=ds_root, cid=1)

        assert assert_api_resp(ret, soft_fail=False)

        ds_file = get_data_from_resp(ret)
        file_id = parse_api_data(ds_file, 'file_id')

        ret = self.case.download_ds_file(file_id=file_id)

        data = ret.content
        assert type(data) == bytes
        assert data == file_data
        assert file_size == len(data)

        ret = self.case.delete_ds_file(file_id)
        assert assert_api_resp(ret, soft_fail=False)