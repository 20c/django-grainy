import six
import inspect
from grainy.core import (
    PermissionSet,
)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import GrainyHandler
from .conf import PERM_CHOICES

def convert_flags(flags):
    """
    Converts string permission flags into integer permission flags
    
    Arguments:
        - flags <str>: one or more flags as they are defined in GRAINY_PERM_CHOICES
            
            For example: "crud" or "ru" or "r"
    
    Returns:
        - int
    """

    r = 0
    if not flags:
        return r

    if isinstance(flags, six.integer_types):
        return flags

    if not isinstance(flags, six.string_types):
        raise TypeError("`flags` needs to be a string or integer type")

    for f in flags:
        for f_i, name, f_s in PERM_CHOICES:
            if f_s == f:
                r = r | f_i
    return r


def namespace(target):

    """
    Convert `target` to permissioning namespace

    Arguments:
        - target <object|class|string>: if an object or class is passed here it 
            will be required to contain a `Grainy` meta class, otherwise a 
            TypeError will be raised.

    Returns:
        - string
    """

    if not target:
        return ""

    handler_class = getattr(target, "Grainy", None)

    if inspect.isclass(handler_class) and issubclass(handler_class, GrainyHandler):
        if inspect.isclass(target):
            return target.Grainy.namespace()
        return target.Grainy.namespace(instance=target)


    if isinstance(target, six.string_types):
        return target

    raise TypeError("`target` {} could not be convered to a permissioning namespace".format(target))

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
            - target <object|class|string>: check permissions to this object / namespace
            - permissions <int|string>: permission flags to check

        Keyword Arguments:
            - explicit <bool>: require explicit permissions to the complete target
                namespsace
        """
        return self.pset.check(namespace(target), convert_flags(permissions), explicit=explicit)

    def apply(self, data):
        return self.pset.apply(data)
