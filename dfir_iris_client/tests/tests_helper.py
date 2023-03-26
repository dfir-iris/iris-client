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
import os
import unittest
from pathlib import Path
from time import sleep

import requests
from dotenv import load_dotenv

from dfir_iris_client.helper.docker_helper import DockerHelper
from dfir_iris_client.helper.utils import assert_api_resp, get_data_from_resp, parse_api_data
from dfir_iris_client.session import ClientSession

API_KEY = os.getenv('IRIS_ADM_API_KEY')
API_URL = os.getenv('IRIS_URL', default="http://127.0.0.1:8000")
COMPOSE_FILE = os.getenv('COMPOSE_FILE', default="../../../iris-web/docker-compose.yml")


def new_session():
    """ """
    session = ClientSession(apikey=API_KEY,
                            host=API_URL, ssl_verify=False)

    return session


def new_adm_session(session: ClientSession = None):
    """ """
    dot_path = Path(__file__).parent / "resources" / ".env"
    if not load_dotenv(dotenv_path=dot_path, override=True):
        raise FileNotFoundError(f"File {dot_path} not found")

    docker_compose = None

    if os.getenv('TEST_WITH_DOCKER', default=False):
        docker_compose = DockerHelper(docker_compose_path=COMPOSE_FILE)
        docker_compose.start()

    while True:
        try:
            requests.head(API_URL, timeout=500)
            break
        except ConnectionError:
            sleep(1)
            pass

    if session is None:
        session = ClientSession(apikey=os.getenv('IRIS_ADM_API_KEY', API_KEY),
                                host=API_URL, ssl_verify=False, timeout=500)

    return session, docker_compose


class InitIrisClientTest(unittest.TestCase):
    docker_compose = None
    session = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.session, cls.docker_compose = new_adm_session(session=cls.session)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.docker_compose is not None:
            cls.docker_compose.stop()

        if cls.session._do_trace:
            print('Writing traces')
            from pathlib import Path
            import datetime
            import json

            traces_dir = Path(__file__).parent / 'traces'
            if not traces_dir.exists():
                traces_dir.mkdir()
            trace_file = traces_dir / f'{datetime.datetime.now()}.json'

            with open(trace_file, 'w') as f:
                f.write(json.dumps(cls.session._trace, indent=4))

            print(f'Traces written in {trace_file}')

    @staticmethod
    def assertIrisPermissionDenied(method: callable, *args, **kwargs) -> None:
        """
        Assert that the method raise an IrisClientException with the message "Permission denied"

        Args:
            method: Method to call and assert

        Returns:
            None
        """
        try:
            method(*args, **kwargs)
        except Exception as e:
            assert "Permission denied" in str(e)


def create_standard_user(session, suffix: str = None):
    """
    Create a new standard user
    """
    login = session.standard_user.login if suffix is None else f"{session.standard_user.login}_{suffix}"
    username = session.standard_user.username if suffix is None else f"{session.standard_user.username}_{suffix}"
    email = session.standard_user.email if suffix is None else f"{session.standard_user.email}_{suffix}"

    ret = session.adm.add_user(login=login,
                               name=username,
                               password=session.standard_user.password,
                               email=email)

    assert assert_api_resp(ret, soft_fail=False)

    data = get_data_from_resp(ret)
    api_key = parse_api_data(data, 'user_api_key')
    session.standard_user.api_key = api_key

    return ret


def get_standard_user_session(session):
    """
    Get a session with standard user
    """
    return ClientSession(apikey=session.standard_user.api_key,
                         host=API_URL, ssl_verify=False)


def delete_standard_user_auto(session, suffix: str = None):
    """
    Delete user
    """
    login = session.standard_user.login if suffix is None else f"{session.standard_user.login}_{suffix}"
    ret = session.adm.deactivate_user(login)
    assert assert_api_resp(ret, soft_fail=False)

    ret = session.adm.delete_user(login)
    assert assert_api_resp(ret, soft_fail=False)

    return ret


def create_standard_group(session):
    """
    Create a new standard group
    """
    return session.adm.add_group(group_name=session.standard_group.name,
                                 group_description=session.standard_group.description,
                                 group_permissions=session.standard_group.permissions)


def delete_standard_group(session):
    """
    Delete group
    """

    return session.adm.delete_group(session.standard_group.name)


def get_random_string(length: int = 10):
    """
    Get a random string
    """
    import random
    import string

    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
