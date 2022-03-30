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

class IrisStatus(object):
    """Defines a custom status class, used by the abstraction layer
    to communicate about API and operations feedbacks

    Args:

    Returns:

    """
    def __init__(self, message=None, data=None, uri=None, is_error=False):
        """
         Mimics the JSON feedback returned by the API

         Args:
            message: Message from the server about the request
            data: Data from the server
            uri: URI that was requested
            is_error: True if the status is an error, else False
        """
        self.message = message
        self.data = data
        self.uri = uri
        self._is_error = is_error

    def __bool__(self):
        """Defines the boolean state of IrisStatus"""
        return not self._is_error

    def __str__(self):
        """Defines the standard str of IrisStatus"""
        msg = ""
        if self.uri:
            msg += f"{self.uri} - "
        if self.message:
            msg += f"{self.message} - "
        if self.data:
            msg += f"{self.data}"
        if len(msg) == 0 and not self._is_error:
            msg = "Success"
        else:
            msg = "Unspecified error" if not msg else msg

        return msg

    def is_error(self) -> bool:
        """Simply return true if status is an error

        Args:

        Returns:
            bool
        """
        return self._is_error

    def is_success(self) -> bool:
        """Simply return true if status is a success
        
        :return: True if status is a success

        Args:

        Returns:
            bool
        """
        return not self._is_error

    def set_error(self) -> None:
        """Force the status to error

        Args:

        Returns:
            None
        """
        self._is_error = True

    def set_success(self) -> None:
        """Force the status to success

        Args:

        Returns:
            None
        """
        self._is_error = False

    pass


class IrisStatusError(IrisStatus):
    """Overlay of IrisStatus, defining a base error status"""
    def __init__(self, message=None, data=None, uri=None):
        super().__init__(message=message, data=data, uri=uri, is_error=True)


class IrisStatusSuccess(IrisStatus):
    """Overlay of IrisStatus, defining a base success status"""
    def __init__(self, message=None, data=None, uri=None):
        super().__init__(message=message, data=data, uri=uri, is_error=False)


class OperationSuccess(IrisStatusSuccess):
    """ """
    pass


BaseOperationSuccess = OperationSuccess()


class OperationFailure(IrisStatusError):
    """ """
    pass


class InvalidObjectMapping(IrisStatusError):
    """ """
    pass


class InvalidCaseId(IrisStatusError):
    """ """
    pass


class InvalidObjectId(IrisStatusError):
    """ """
    pass


class ObjectNotFound(IrisStatusError):
    """ """
    pass


class InvalidObjectType(IrisStatusError):
    """ """
    pass


class CaseNotInitialized(IrisStatusError):
    """ """
    pass


class ApiRequestFailure(IrisStatusError):
    """ """
    pass


class InvalidApiResponse(IrisStatusError):
    """ """
    pass


class ObjectNotInitialized(IrisStatusError):
    """ """
    pass


class ObjectAlreadyInitialized(IrisStatusError):
    """ """
    pass