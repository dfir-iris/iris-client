import os

from dfir_iris_client.case import Case
from dfir_iris_client.session import ClientSession
from dfir_iris_client.helper.utils import parse_api_data, get_data_from_resp, assert_api_resp

import logging
import os

LOG_FORMAT = '%(asctime)s %(levelname)s %(funcName)s: %(message)s'

logging.basicConfig(format=LOG_FORMAT, level='INFO', datefmt='%Y-%m-%d %I:%M:%S')
log = logging.getLogger(__name__)

# Initiate a session with our API key and host. Session stays the same during all the script run.
session = ClientSession(apikey=os.environ.get('IRIS_API_KEY'),
                        host='https://127.0.0.1:4433', ssl_verify=False)

# Initialize the case instance with the session
case = Case(session=session)

# Create a new case. The create_customer creates the customer if it doesn't exists, otherwise the method
# would turn an error. This implies the calling user has administrative role.
status = case.add_case(case_name='A new case',
                       case_description='Short initial description, or really long '
                                        'description. It\'s up to you',
                       case_customer='IrisClientApiDemo',
                       soc_id='soc_11',
                       create_customer=True)

# Always check the status as most of the methods do not raise exceptions. Setting soft_fail = False tells the client
# to raise an exception if the request failed
assert_api_resp(status, soft_fail=False)

# The case ID is returned by the server in case of success. We need this case ID for the next steps
# Status are ApiResponse objects, and contains answers from the server.
# While the ID could be retrieved with status.get_data().get('case_id'), it is preferable to use
# the overlays get_data_from_resp and parse_api_data to be future proof, in case response from server are changed.
case_data = get_data_from_resp(status)
case_id = parse_api_data(case_data, 'case_id')

log.info(f'Created case ID {case_id}')

# Set the case instance with the new case ID. From now one, every action done with a method of the case instance
# will be done under this case ID.
# This can be used to directly modify existing cases etc
case.set_cid(case_id)


# Let's add an IOC to our case
# As in the GUI, not all attributes are mandatory. For instance here we have omitted everything not mandatory
# Most of the methods autor esolve the types names. Here we set an IOC as AS directly, without specifying which ID is
# and IOC AS type
status_ioc = case.add_ioc(value='API IOC AS', ioc_type='AS')

# We keep to ioc ID so we can add it to an asset later
ioc_data = get_data_from_resp(status_ioc)
ioc_id = parse_api_data(ioc_data, 'ioc_id')

log.info(f'Created IOC ID {ioc_id}. Server returned {status_ioc}')

# Let's add an asset and associate the ioc with an update
status_asset = case.add_asset(name='API asset', asset_type='Windows - Computer',
                              description='A comprehensive description', compromised=True, analysis_status='Started')
assert_api_resp(status_asset, soft_fail=False)

# We keep to asset ID so we can add it
asset_data = get_data_from_resp(status_asset)
asset_id = parse_api_data(asset_data, 'asset_id')

log.info(f'Created asset ID {asset_id}')

# Update the asset with the new ioc. By letting all fields empty except ioc_links, we only update this field.
status_asset = case.update_asset(asset_id=asset_id, ioc_links=[ioc_id])
assert_api_resp(status, soft_fail=False)

log.info(f'Asset updated. Data :  {status_asset.as_json()}')

# Add some notes groups
status_gp1 = case.add_notes_group('API group 1')
assert_api_resp(status_gp1, soft_fail=False)

log.info(f'Created API group 1 notes group')


status_gp2 = case.add_notes_group('API group 2')
assert_api_resp(status_gp2, soft_fail=False)

log.info(f'Created API group 2 notes group')


status_gp3 = case.add_notes_group('API group 3')
assert_api_resp(status_gp3, soft_fail=False)

log.info(f'Created API group 3 notes group')

# Get the group_id of Group 2 and add some notes
group_2_data = get_data_from_resp(status_gp2)
group_2_id = parse_api_data(data=group_2_data, path='group_id')

status_note = case.add_note(note_title='API note 1 for group 2',
                            note_content='Anything you want really',
                            group_id=group_2_id)
assert_api_resp(status_note, soft_fail=False)
log.info(f'Created note API note 1 for group 2')


status_note = case.add_note(note_title='API note 2 for group 2',
                            note_content='Anything you want really',
                            group_id=group_2_id)
assert_api_resp(status_note, soft_fail=False)
log.info(f'Created note API note 2 for group 2')



