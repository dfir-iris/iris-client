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
from abc import abstractmethod

from dfir_iris_client.case import Case
from dfir_iris_client.helper.errors import IrisStatus, \
    BaseOperationSuccess, OperationFailure, ObjectNotInitialized
from dfir_iris_client.helper.utils import get_iris_session, map_object

"""
For future use only
"""


class iris_obj_property(object):
    """Defines a custom property allowing to automatically flip the sync state of an IrisObject.
    When a iris_obj_property property is set, the corresponding IrisObject is set to desync state.
    This allows to keep tracks of changes committed to the server.

    Args:

    Returns:

    """
    def __init__(self, field, fget=None, fset=None):
        self.field = field
        self.fget = fget
        self.fset = fset

    def __get__(self, instance, field) -> any:
        """
        Getter of the property. Returns the requested value from the IrisObject.
        The property act as an overlay over the real attribute of the object.
        The schema is property_name = _attribute_name.

        For example, getting the value of case.name results in the attribute case._name being returned.

        Args:
            instance: IrisObject instance
            field: Field to return.

        Returns:
            The attribute
        """
        if self.fget:
            return self.fget(instance, field)

        return getattr(instance, f"_{self.field.__name__}")

    def __set__(self, instance, value) -> None:
        """
        Setter of the property. As for the getter, it acts as an overlay over the real attribute of the object.
        The schema is the same.  property_name = _attribute_name.

        For example, setting case.name = "My value", actually results in case._name = "My value".

        Once the set is done, the instance._set_unsynced() is called to flip the sync state of the IrisObject.

        Args:
            instance: IrisObject instance
            value: Value to set the attribute with

        Returns:
            None
        """
        if self.fset:
            return self.fset(instance, value)

        setattr(instance, f"_{self.field.__name__}", value)
        instance._set_unsynced()

    def getter(self, fget):
        """Setter of the getter

        Args:
          fget: Getter method

        Returns:
            None
        """
        return type(self)(self.field, fget, self.fset)

    def setter(self, fset):
        """Setter of the setter

        Args:
          fset: Setter method

        Returns:
            None
        """
        return type(self)(self.field, self.fget, fset)


class iris_dynamic_property(object):
    """Defines a custom property similar to `iris_obj_property`, allowing to automatically
    flip the sync state of an IrisObject. In addition, it allows the handling of partially loaded instances.
    
    Here is why partial IrisObjects (called IrisDynamicObject) are necessary.
    Let's say a user list all events with case.timeline. This will results of the loading of all events.
    However, events contains a link to assets. And assets a link to iocs. So loading the timeline would results in
    the loading and instanciation of almost all data of the case. This could be fine, but if the user only deals with
    a few events like changing the category, then all the data would have been loaded for nothing.
    
    timeline
        + event 1  - fully loaded by default
            + asset 1 - fully loaded by default
                + ioc 2 - fully loaded by default
            + asset 2 - fully loaded by default
                + ioc 1 - fully loaded by default
                + ioc 2 - fully loaded by default
        + event 2 - fully loaded by default
            + asset 3 - fully loaded by default
                + ioc 5 - fully loaded by default
            + asset 4 - fully loaded by default
    
    
    If the user wants to get the asset 4 of event 2, it has to load everything (or get the event itself only but some
    people might just do it this way).
    
    To avoid that, IrisDynamicObject implement partial loading thanks to iris_dynamic_property properties.
    In the above example, this results in all events being initialised, but each events will only partially load
    the level of children. It actually only loads the data needed to load the child in case it is accessed (usually name
    and object ID).
    If a child is accessed, then it's fully loaded and in turn partially load its own children,
    etc. The above schema to access asset 3 of event 2 results then in the following.
    
    timeline
    + event 1  - fully loaded by default
        + asset 1 - partially loaded
        + asset 2 - partially loaded
    + event 2 - fully loaded by default
        + asset 3 - fully loaded upon user access
            + ioc 5 - partially loaded
        + asset 4 - partially loaded
    
    As for iris_obj_property, when a property is set, the corresponding IrisObject is set to the desync state.
    This allows to keep tracks of changes to committed to the server.

    Args:

    Returns:

    """
    def __init__(self, field, fget=None, fset=None):
        self.field = field
        self.fget = fget
        self.fset = fset

    def __get__(self, instance, field) -> any:
        """
        Getter of the property. The getter verifies the state of the IrisDynamicObject instance and returns
        the corresponding attribute if the instance is not partial and not synced.

        If the instance is partial, then the base method init_from_id is called. This implies that the instance
        ID has been set. This has to be done by methods when they partially initialize an object.
        If this is not the case or the init fails an Exception(ObjectNotInitialized()) exception is raised.
        Once the loading is done, the partial state of the IrisDynamicObject is flipped.

        Like iris_obj_property, the property act as an overlay over the real attribute of the object.
        The schema is property_name = _attribute_name.

        For example, getting the value of case.name results in the attribute case._name being returned.

        Args:
            instance: IrisObject instance
            field: Field to return

        Returns:
            The attribute
        """
        if self.fget:
            return self.fget(instance)

        if instance._is_partial and instance._is_synced:
            ret = instance.init_from_id(instance.id)
            if not ret: raise Exception(ObjectNotInitialized(str(ret)))

            instance._is_partial = False

        return getattr(instance, f"_{self.field.__name__}")

    def __set__(self, instance, value):
        """
        Setter of the property. As for the getter, it acts as an overlay over the real attribute of the object.
        The schema is the same.  property_name = _attribute_name.

        If the instance is partial, then the base method init_from_id is called. This implies that the instance
        ID has been set. This has to be done by methods when they partially initialize an object.
        If this is not the case or the init fails an Exception(ObjectNotInitialized()) exception is raised.
        Once the loading is done, the partial state of the IrisDynamicObject is flipped.
        After that, the property is set.

        For example, setting case.name = "My value", actually results in case._name = "My value".

        Once the set is done, the instance._set_unsynced() is called to flip the sync state of the IrisObject.

        Args:
            instance: IrisObject instance
            value: Value to set the attribute with

        Returns:
            None
        """
        if self.fset:
            return self.fset(instance, value)

        if instance._is_partial and instance._is_synced:
            ret = instance.init_from_id(instance.id)
            if not ret: raise Exception(ObjectNotInitialized(str(ret)))
            instance._is_partial = False

        setattr(instance, f"_{self.field.__name__}", value)
        instance._set_unsynced()

    def getter(self, fget):
        """Setter of the getter

        Args:
          fget: Getter

        Returns:

        """
        return type(self)(self.field, fget, self.fset)

    def setter(self, fset):
        """Setter of the setter

        Args:
          fset: Setter

        Returns:

        """
        return type(self)(self.field, self.fget, fset)


class IrisObject(object):
    """Defines a standard IrisObject. These are used by the abstraction layer of the client.
    They automatically find the ClientSession and implement the basic attributes and methods
    allowing the abstraction layer to function.

    Args:

    Returns:

    """
    object_name = "base"

    def __init__(self, cid: int = None):
        """
        Fetch the client session and initiate a case helper class with the provided CID.
        The CID at init is not mandatory and can be set later on with set_cid. However this needs
        to be done before any method of the class is called, otherwise the CaseHelper won't know to
        with which case it needs to talk to.
        By default, objects are initiated in an unsynced state.

        """
        from dfir_iris_client.session import ClientSession
        self._s: ClientSession = get_iris_session()
        self._ch = Case(session=self._s, case_id=cid)

        self._cid = cid
        self._id = None
        self._is_synced = False

    def __int__(self):
        return self._id

    def set_cid(self, cid: int) -> IrisStatus:
        """Set the case ID and propagate to the helper class

        Args:
          cid: Case ID

        Returns:
          IrisStatus object

        """
        self._cid = cid
        self._ch.set_cid(cid)

        return BaseOperationSuccess

    def set_id(self, id: int) -> None:
        """Set the ID of the IrisObject instance. This represents the ID of the corresponding object on the server.

        Args:
          id: ID of the object

        Returns:
          None

        """
        self._id = id

    @property
    def id(self) -> int:
        """ """
        return self._id

    @property
    def is_synced(self) -> bool:
        """Light wrapper around the sync state"""
        return self._is_synced

    def _set_sync_state(self, state: bool) -> None:
        """Internal method to flip the sync state

        Args:
          state: bool: Sync state to set

        Returns:
            IrisStatus
        """
        self._is_synced = state

    def _set_unsynced(self):
        """Set the instance to unsynced state"""
        self._is_synced = False

    def init_from_id(self, id: int = None) -> IrisStatus:
        """Every object need to implement this initialisation method. Failing to do so results in exception

        Args:
          id: int:  ID of object to init (Default value = None)

        Returns:
            IrisStatus
        """
        raise Exception(OperationFailure('Operation not implemented'))

    def init_from_data(self, data: dict) -> IrisStatus:
        """Every object need to implement this initialisation method. Failing to do so results in exception

        Args:
          data: dict: Init data

        Returns:
            IrisStatus
        """
        raise Exception(OperationFailure('Operation not implemented'))

    def sync(self) -> IrisStatus:
        """Force the synchronization of the object with the server.
        
        !!! warning Any local unsaved changes will be erase

        Args:

        Returns:
            IrisStatus
        """
        self.reset(keep_id=True, keep_cid=True)

        ret = self.init_from_id(id=self.id)
        self._is_synced = ret.is_success()

        return ret

    def reset(self, keep_id=False, keep_cid=False):
        """Resets an IRIS object. Acts as a new object.

        Args:
          keep_id: If set, the object will keep its current ID. (Default value = False)
          keep_cid: If set, the object will keep its current Case ID cid. (Default value = False)

        Returns:

        """
        id = self.id if keep_id else None
        cid = self._cid if keep_cid else None

        self.__init__()
        self.set_id(id)
        self.set_cid(cid)


class IrisDynamicObject(IrisObject):
    """Defines an overlay of IrisObject, by providing additional attribute needed to keep track of the partial state"""

    def __init__(self,  cid: int = None):
        """Call IrisObject init and set partial state by default"""
        super().__init__(cid=cid)
        self._is_partial = False

    @property
    def is_partial(self) -> bool:
        """ """
        return self._is_partial

    def init_from_data(self, data: dict, partial: bool = False) -> IrisStatus:
        """Init the object from an API data response. Set the sync state according to the init operation return.

        Args:
          data: API data response
          partial: Partial load of the object

        Returns:
          IrisStatus

        """
        self._is_partial = partial
        ret = map_object(self, data)

        self._set_sync_state(ret.is_success())

        return ret