from grainy.core import (
    PermissionSet,
)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import (
    namespace,
)
from .helpers import (
    int_flags,
    str_flags
)

class Permissions(object):

    """
    A utility class that will allow you to perform permission checks
    for a user or group on cached permission sets
    """

    def __init__(self, obj):
        """
        Arguments:
            - obj <User|Group>
        """
        if not isinstance(obj, get_user_model()) and not isinstance(obj, Group):
            raise ValueError(
                "`obj` needs to be either of type `{}` or `Group`".format(
                    get_user_model().__class__.__name__
                )
            )
        self.obj = obj
        self.pset = PermissionSet()
        self.loaded = False
        self.load()

    def load(self, refresh=False):
        """
        Loads the permission set for the user or group specified in
        `self.obj` 

        Keyword Arguments:
            - refresh <bool>: if True, permission set will be reloaded if it
                has been loaded before
        """
        if not self.loaded or refresh:
            self.pset = self.obj.grainy_permissions.permission_set()
            if isinstance(self.obj, get_user_model()):
                # if we are loading permissions for user, we need
                # to also merge in permissions from any of the 
                # groups the user is a part of
                for group in self.obj.groups.all():
                    self.pset.update(
                        group.grainy_permissions.permission_set().permissions
                    )

    def check(self, target, permissions, explicit=False):
        """
        Check permissions for the specified target

        Arguments:
            - target <object|class|str>: check permissions to this object / namespace
            - permissions <int|str>: permission flags to check

        Keyword Arguments:
            - explicit <bool>: require explicit permissions to the complete target
                namespsace
        """
        return self.pset.check(namespace(target), int_flags(permissions), explicit=explicit)

    def get(self, target, as_string=False):
        """
        Returns the permission flags for the specified target

        Arguments:
            - target <object|class|str>: return permissions to this object /
                namespsace 
        
        Keyword Arguments:
            - as_string <bool>: if True returns string flags instead of int flags

        Returns:
            - <int>: permission flags
            - <str>: permission flags, if as_string=True
        """
        if as_string:
            return str_flags(self.pset.get_permission(namespace(target)))
        return self.pset.get_permission(namespace(target))

    def apply(self, data):
        return self.pset.apply(data)
