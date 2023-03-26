from dfir_iris_client.case import Case
from dfir_iris_client.session import ClientSession
from dfir_iris_client.helper.utils import parse_api_data, get_data_from_resp, assert_api_resp

from ex_helper import random_date

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

# Fetch the case from its ID. Let's use the initial demo case and improve it
if not case.case_id_exists(cid=1):
    # This should never happen, the server refuses to delete this case for consistency
    raise Exception('Case ID 1 not found !')

# Attribute the cid to the case instance
case.set_cid(cid=1)

# We can now modify the case. Let's add some tasks.
# Again task status and assignee are attribute being looked up before issuing the task addition request.
# For efficiency and avoid unnecessary requests, the IDs can also be provided if they are known.
status = case.add_task(title='Analysis of laptop X',
                       description='Plaso the laptop',
                       assignees=['administrator'],
                       status='To do')

assert_api_resp(status, soft_fail=False)
log.info(f'Created new task : {status.as_json()}')

status = case.add_task(title='Analysis of server Y',
                       assignees=['administrator'],
                       status='In progress')

assert_api_resp(status, soft_fail=False)
log.info(f'Created new task : {status.as_json()}')

# Next add some events if the timeline is empty
status = case.list_events()
assert_api_resp(status, soft_fail=False)

timeline = parse_api_data(status.get_data(), 'timeline')
if len(timeline) < 85:
    for i in range(0, 150):
        # Only title and datetime are required, but here we play with the summary and graphs too
        status = case.add_event(f'Event {i}',
                                date_time=random_date(),
                                display_in_summary=(i % 2 == 0),
                                display_in_graph=(i % 3 == 0))

        # Status object can be check with a boolean expression directly
        if not status:
            status.log_error()
            continue
        log.info(f'Added event {i}')


status = case.add_task_log("Started analysis of computer X")
if not status:
    status.log_error()