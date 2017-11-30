import six
import inspect
from grainy.core import (
    PermissionSet,
)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django_grainy.models import GrainyHandler

def namespace(target):

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
        return self.pset.check(namespace(target), permissions, explicit=explicit)

    def apply(self, data):
        return self.pset.apply(data)
