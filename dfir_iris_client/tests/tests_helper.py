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

from dfir_iris_client.session import ClientSession

API_KEY = ''


def new_session():
    """ """
    session = ClientSession(apikey=API_KEY,
                            host='https://127.0.0.1', ssl_verify=False)

    return session


def new_adm_session():
    """ """
    session = ClientSession(apikey=API_KEY,
                            host='https://127.0.0.1', ssl_verify=False)

    return session

