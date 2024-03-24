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
                        host='http://127.0.0.1:8000', ssl_verify=False)

# Initialize the case instance with the session
case = Case(session=session)

# Create a new case. The create_customer creates the customer if it doesn't exist, otherwise the method
# would turn an error. This implies the calling user has administrative role.
status = case.add_case(case_name='A new case',
                       case_description='Short initial description, or really long '
                                        'description. It\'s up to you',
                       case_customer='IrisClientApiDemo',
                       case_classification='other:other',
                       soc_id='soc_11',
                       create_customer=True)

# Always check the status as most of the methods do not raise exceptions. Setting soft_fail = False tells the client
# to raise an exception if the request fails
assert_api_resp(status, soft_fail=False)

# All the methods are simply overlays of the API itself, so to know exactly what a method answers, one can either try
# it or head to the API reference documentation and lookup the corresponding endpoint.
# The case ID is returned by the server in case of success. We need this case ID for the next steps
# Status are ApiResponse objects, and contains answers from the server.
# While the ID could be retrieved with status.get_data().get('case_id'), it is preferable to use
# the overlays get_data_from_resp and parse_api_data to be future proof, in case response from server are changed.
case_data = get_data_from_resp(status)
case_id = parse_api_data(case_data, 'case_id')

log.info(f'Created case ID {case_id}')

# Set the case instance with the new case ID. From now on, every action done with a method of the case instance
# will be done under this case ID, except if the CID is explicitly provided on the method itself.
# This can be used to directly modify existing cases etc.
case.set_cid(case_id)


# Let's add an IOC to our case
# As in the GUI, not all attributes are mandatory. For instance here we have omitted everything not mandatory
# Most of the methods auto resolve the types names. Here we set an IOC as AS directly, without specifying which ID is
# the IOC AS type
status_ioc = case.add_ioc(value='API IOC AS', ioc_type='AS')

# We keep the ioc ID so we can add it to an asset later
ioc_data = get_data_from_resp(status_ioc)
ioc_id = parse_api_data(ioc_data, 'ioc_id')

log.info(f'Created IOC ID {ioc_id}. Server returned {status_ioc}')

# Let's add an asset and associate the ioc with an update
status_asset = case.add_asset(name='API asset', asset_type='Windows - Computer',
                              description='A comprehensive description', compromise_status=1,
                              analysis_status='Started')
assert_api_resp(status_asset, soft_fail=False)

# We keep the asset ID so we can update it
asset_data = get_data_from_resp(status_asset)
asset_id = parse_api_data(asset_data, 'asset_id')

log.info(f'Created asset ID {asset_id}')

# Update the asset with the new ioc. By letting all fields empty except ioc_links, we only update this field.
status_asset = case.update_asset(asset_id=asset_id, ioc_links=[ioc_id])
assert_api_resp(status, soft_fail=False)

log.info(f'Asset updated. Data :  {status_asset.as_json()}')

# Add some notes directories
status_dir1 = case.add_notes_directory('API Directory 1')
assert_api_resp(status_dir1, soft_fail=False)

log.info(f'Created API directory 1 notes directory')


status_dir2 = case.add_notes_directory('API Directory 2')
assert_api_resp(status_dir2, soft_fail=False)

log.info(f'Created API directory 2 notes directory')


status_dir3 = case.add_notes_directory('API Directory 3')
assert_api_resp(status_dir3, soft_fail=False)

log.info(f'Created API directory 3 notes group')

# Get the group_id of Group 2 and add some notes
dir_2_data = get_data_from_resp(status_dir2)
dir_2_id = parse_api_data(data=dir_2_data, path='id')

status_note = case.add_note(note_title='API note 1 for directory 2',
                            note_content='Anything you want really',
                            directory_id=dir_2_id)
assert_api_resp(status_note, soft_fail=False)
log.info(f'Created note API note 1 for group 2')


status_note = case.add_note(note_title='API note 2 for directory 2',
                            note_content='Anything you want really',
                            directory_id=dir_2_id)
assert_api_resp(status_note, soft_fail=False)
log.info(f'Created note API note 2 for group 2')



