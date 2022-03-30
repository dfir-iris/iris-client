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
from typing import Union

import logging as log
import json

from types import SimpleNamespace

from dfir_iris_client.helper.errors import ApiRequestFailure, InvalidApiResponse, OperationSuccess, IrisStatus, OperationFailure, \
    InvalidObjectMapping, BaseOperationSuccess
from functools import reduce
from dfir_iris_client.helper.objects_def import objects_map


def get_iris_session():
    """Return the global variable client session

    Args:

    Returns:
      ClientSession

    """
    from dfir_iris_client.session import client_session
    if client_session:
        return client_session
    raise Exception('IRIS client session not found')


def map_object(obj, data_obj: dict, obj_type=None, strict=False) -> IrisStatus:
    """Map a Python IrisObject with a known Iris API return. The mapping is done
    thanks to objects_def. Each field is attributed to an attribute of the
    provided obj.
    
    The methods takes advantage of iris_abj_attribute and iris_dynamic_attribute to
    preprocess data if needed.

    Args:
      obj: Object where attributes need to be set
      obj_type: Force the object type. Unused (Default value = None)
      data_obj: Dict describing the data to set
      strict: Set to true to fail if an attribute is missing (Default value = False)

    Returns:
      IrisStatus

    """
    if obj is None:
        return OperationFailure('Unable to map object. Provided object is null')

    obj_def = objects_map.get(obj.object_name)
    if not obj_def:
        raise Exception(InvalidObjectMapping(f'Unrecognised {obj_def} for mapping'))

    for attribute in obj_def:

        field = obj_def[attribute]
        if not hasattr(obj, attribute) and strict:
            obj_type = obj_type if obj_type else obj.object_name
            raise Exception(InvalidObjectMapping(message=f'Invalid object mapping for {obj_type}. Missing attribute'
                                                 f' {attribute} for {field}',
                                                 data=data_obj))
        if field not in data_obj and strict:
            obj_type = obj_type if obj_type else obj.object_name
            raise Exception(InvalidObjectMapping(message=f'Invalid object mapping for {obj_type}. Missing field'
                                                 f' {field} in server data',
                                                 data=data_obj))

        if attribute == 'id':
            obj.set_id(data_obj.get(field))

        else:
            setattr(obj, attribute, data_obj.get(field))

    return BaseOperationSuccess


class ApiResponse(object):
    """Handles API returns and error. It parses the standard API returns and build an
    standard ApiResponse object.

    Args:

    Returns:

    """
    def __init__(self, response: json = None, uri: str = None):
        try:

            self._response = json.loads(response)

        except Exception as e:
            log.error(e)

        if not response:
            raise Exception("Empty response")

        self._uri = uri

    def __repr__(self):
        return json.dumps(self.as_json())

    def __bool__(self):
        return self.is_success()

    def is_error(self):
        """:return: Bool - True if return is error"""
        if not hasattr(self, "_response"):
            return True

        if self._response.get('status') != "success":
            return True
        return False

    def is_success(self):
        """:return: Bool - True if return is success"""
        if not hasattr(self, "_response"):
            return False

        if self._response.get('status') == "success":
            return True
        return False

    def get_data(self):
        """ """
        if not hasattr(self, "_response"):
            return None

        return self._response.get('data')

    def get_msg(self):
        """ """
        if not hasattr(self, "_response"):
            return None

        return self._response.get('message')

    def get_uri(self):
        """ """
        return self._uri

    def as_json(self):
        """ """
        if not hasattr(self, "_response"):
            return None

        return self._response

    def log_error(self):
        """ """
        errors = self.get_data()
        log.error(f'{self._uri} :: {self.get_msg()}')

        if errors:
            for e in errors:
                log.error("{item} : {error}".format(item=e, error=errors[e]))


def get_data_from_resp(api_response: ApiResponse):
    """Returns the data of an ApiResponse object

    Args:
      api_response: ApiResponse: 

    Returns:

    """
    return api_response.get_data()


def assert_api_resp(api_response: ApiResponse, soft_fail=True) -> IrisStatus:
    """Convert an ApiResponse to an IrisStatus for the overlay

    Args:
      api_response: ApiResponse: Object to assert
      soft_fail:  Set to false to raise exception (Default value = True)

    Returns:

    """
    if api_response.is_error():
        if soft_fail:
            return ApiRequestFailure(message=api_response.get_msg(),
                                     data=api_response.get_data(),
                                     uri=api_response.get_uri())
        else:
            raise Exception(ApiRequestFailure(message=api_response.get_msg(),
                                              data=api_response.get_data(),
                                              uri=api_response.get_uri()))

    return OperationSuccess(message=api_response.get_msg(),
                            data=api_response.get_data(),
                            uri=api_response.get_uri())


def parse_api_data(data: dict, path: Union[list, str], strict=True) -> any:
    """Parses the data field of an API response. Path describes a path to fetch a specific value in data.
    If strict is set, an exception is raised, otherwise None is returned.

    Args:
      data: Dict from the API response
      path: Value to get from within data
      strict: Set to true to fails if path is not found in data (default)

    Returns:
      ApiResponse

    """
    if not isinstance(data, dict):
        if strict:
            raise Exception(InvalidApiResponse(message=f'Object {path} not found in API response {data}'))
        else:
            return None

    ori_path = path
    if isinstance(path, str):
        path = [path]

    fdata = reduce(dict.get, path, data)
    if fdata is None and ori_path not in data:
        if strict:
            raise Exception(InvalidApiResponse(message=f'Object {path} not found in API response {data}'))
        else:
            return None

    return fdata


def ClientApiError(error=None, msg=None):
    """

    Args:
      error:  (Default value = None)
      msg:  (Default value = None)

    Returns:

    """
    resp = {
        "data": [error] if error else [],
        "message": msg if msg else "This response was generated client-side",
        "status": "error"
    }
    return ApiResponse(json.dumps(resp))


EmptyApiResponse = ApiResponse('''{
    "data": [],
    "message": "This response was generated client-side",
    "status": "error"
}''')


def ClientApiData(message=None, data=None, status=None):
    """

    Args:
      message:  (Default value = None)
      data:  (Default value = None)
      status:  (Default value = None)

    Returns:

    """
    resp = {
        "data": data if data else [],
        "message": message if message else "This response was generated client-side",
        "status": status if status else "success"
    }
    return json.dumps(resp)
