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

from dfir_iris_client.helper.utils import ApiResponse, ClientApiError
from dfir_iris_client.session import ClientSession


def global_search_ioc(session: ClientSession, search_term: str) -> ApiResponse:
    """
    Searches an IOC across all investigation

    :param session: Client Session to use for request
    :param search_term: Search term to search for IOC
    :return: ApiResponse object
    """
    if not session:
        return ClientApiError(msg=f'session is not a valid. Expected ClientSession got {type(session)}')

    if not search_term:
        return ClientApiError(msg='search_term cannot be null. Use % for wildcard')

    body = {
        "search_value": search_term,
        "search_type": "ioc",
        "cid": 1
    }

    return session.pi_post('search', data=body)


def global_search_notes(session: ClientSession, search_term: str) -> ApiResponse:
    """
    Searches in note contents across all investigation

    :param session: Client Session to use for request
    :param search_term: Search term to search for notes
    :return: ApiResponse object
    """
    if not session:
        return ClientApiError(msg=f'session is not a valid. Expected ClientSession got {type(session)}')

    if not search_term:
        return ClientApiError(msg='search_term cannot be null. Use % for wildcard')

    body = {
        "search_value": search_term,
        "search_type": "notes",
        "cid": 1
    }

    return session.pi_post('search', data=body)