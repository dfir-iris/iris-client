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
from dfir_iris_client.session import ClientSession

API_KEY = os.getenv('IRIS_ADM_API_KEY')
API_URL = os.getenv('IRIS_URL', default="http://127.0.0.1:8000")
COMPOSE_FILE = os.getenv('COMPOSE_FILE', default="../../../iris-web/docker-compose.yml")


def new_session():
    """ """
    session = ClientSession(apikey=API_KEY,
                            host=API_URL, ssl_verify=False)

    return session


def new_adm_session():
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
            count = 0
            while count < 5:
                requests.head(API_URL, timeout=500)
                count += 1
                sleep(1)
            break
        except ConnectionError:
            pass

    session = ClientSession(apikey=os.getenv('IRIS_ADM_API_KEY', API_KEY),
                            host=API_URL, ssl_verify=False, timeout=500)

    return session, docker_compose


class InitIrisClientTest(unittest.TestCase):
    docker_compose = None
    session = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.session, cls.docker_compose = new_adm_session()

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.docker_compose is not None:
            cls.docker_compose.stop()
