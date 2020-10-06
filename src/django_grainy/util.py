from grainy.core import PermissionSet, Applicator

from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, AnonymousUser

from .helpers import namespace, int_flags, str_flags
from .conf import ANONYMOUS_PERMS


class Permissions:

    """
    A utility class that will allow you to perform permission checks
    for a user or group on cached permission sets
    """

    def __init__(self, obj):
        """
        Arguments:
            - obj <User|AnonymousUser|Group|Model>
        """

        if not hasattr(obj, "grainy_permissions") and not isinstance(
            obj, AnonymousUser
        ):
            raise ValueError(
                "`obj` needs to be have a `grainy_permissions` relationship"
            )
        self.obj = obj
        self.pset = PermissionSet()
        self.applicator = Applicator(self.pset)
        self.loaded = False
        self.load()

        self.grant_all = isinstance(obj, get_user_model()) and obj.is_superuser

    def load(self, refresh=False):
        """
        Loads the permission set for the user or group specified in
        `self.obj`

        In case `self.obj` holds an `AnonymousUser` instance, perms are loaded
        from settings.GRAINY_ANONYMOUS_PERMS

        Keyword Arguments:
            - refresh <bool>: if True, permission set will be reloaded if it
                has been loaded before
        """
        if not hasattr(self.obj, "grainy_permissions"):
            if isinstance(self.obj, AnonymousUser):
                # Permission for AnonymousUser instance are loaded from
                # settigns
                if not self.loaded or refresh:
                    self.pset = PermissionSet(ANONYMOUS_PERMS)
                    self.loaded = True
            return

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
            self.loaded = True

    def check(self, target, permissions, explicit=False, ignore_grant_all=False):
        """
        Check permissions for the specified target

        Arguments:
            - target <object|class|str>: check permissions to this object / namespace
            - permissions <int|str>: permission flags to check

        Keyword Arguments:
            - explicit <bool>: require explicit permissions to the complete target
                namespsace
            - ignore_grant_all <bool>: if True the `grant_all` property will be ignored
                during permission checks. If false, users with the `superuser` status will
                automatically pass all the permission checks.
        """
        if self.grant_all and not ignore_grant_all:
            return True
        return self.pset.check(
            namespace(target), int_flags(permissions), explicit=explicit
        )

    def get(self, target, as_string=False, explicit=False):
        """
        Returns the permission flags for the specified target

        Arguments:
            - target <object|class|str>: return permissions to this object /
                namespsace

        Keyword Arguments:
            - as_string <bool>: if True returns string flags instead of int flags
            - explicit <bool>: require explicit permissions to the complete target

        Returns:
            - <int>: permission flags
            - <str>: permission flags, if as_string=True
        """
        if as_string:
            return str_flags(
                self.pset.get_permissions(namespace(target), explicit=explicit)
            )
        return self.pset.get_permissions(namespace(target), explicit=explicit)

    def apply(self, data):
        """
        Applies permissions to the specified data, removing all content that
        is not permissioned on a READ level

        Arguments:
            - data <dict>

        Returns:
            - dict: sanitized data
        """
        if self.grant_all:
            return data
        self.applicator.pset = self.pset
        return self.pset.apply(data, applicator=self.applicator)

    def instances(self, model, permissions, explicit=False, ignore_grant_all=False):
        """
        Return a list of all instances of the specified model that
        are permissioned at the specified level

        Arguments:
            - model <Model|QuerySet>
            - permissions <str|int>: permission flag(s)

        Keyword Arguments:
            - explicit <bool>: require explicit permissions to the complete target
                namespsace
            - ignore_grant_all <bool>: if True the `grant_all` property will be ignored
                during permission checks. If false, users with the `superuser` status will
                automatically pass all the permission checks.

        Returns:
            - list: model instances
        """

        if isinstance(model, QuerySet):
            q = model
        else:
            q = model.objects.all()

        return [
            instance
            for instance in q
            if self.check(
                instance,
                permissions,
                explicit=explicit,
                ignore_grant_all=ignore_grant_all,
            )
        ]
