from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from grainy.const import PERM_READ
from grainy.core import PermissionSet

from .fields import PermissionField
from .helpers import int_flags, namespace


class PermissionQuerySet(models.QuerySet):
    """
    Queryset that offers additional utilities for UserPermission and
    GroupPermission queries
    """

    def permission_set(self):
        """
        Builds and returns a grainy.PermissionSet object from all
        the rows in the query

        Returns:
            - grainy.PermissionSet
        """
        pset = PermissionSet()
        for row in self:
            pset[row.namespace] = row.permission
        return pset


class PermissionManager(models.Manager):
    """
    Object Manager that offers additional utilities for managing
    UserPermission and GroupPermission objects
    """

    def get_queryset(self):
        return PermissionQuerySet(self.model, using=self._db)

    def add_permission_set(self, pset):
        """
        Add all permissions specified in a PermissionSet

        Arguments:
            - pset <grainy.PermissionSet|dict>: if passed as `dict` permission
                values may be passed as string flags
        """

        _pset = self.permission_set()

        if not isinstance(pset, PermissionSet) and isinstance(pset, dict):
            pset = PermissionSet({ns: int_flags(f) for ns, f in list(pset.items())})

        for _namespace, permission in list(pset.permissions.items()):
            _pset[_namespace] = permission

        for _namespace, permission in list(_pset.permissions.items()):
            self.update_or_create(
                namespace=_namespace, defaults={"permission": permission.value}
            )

    def add_permission(self, target, permission):
        """
        Add permission for the specified target

        Arguments:
            - target <object|class|str>
            - permission <str|int>: permission flags
        """

        self.update_or_create(
            namespace=namespace(target), defaults={"permission": int_flags(permission)}
        )

    def delete_permission(self, target):
        """
        Remove an explicit permission rule set for the
        specified target.

        Note that this does not touch permissions granted
        by rulings higher up in the namespace path

        Arguments:
            - target <object|class|str>
        """

        self.get_queryset().filter(namespace=namespace(target)).delete()

    def permission_set(self):
        """
        Return grainy.PermissionSet instance from all rows returned
        from get_queryset()

        Returns:
            - grainy.PermissionSet
        """
        return self.get_queryset().all().permission_set()


# Create your models here.


class Permission(models.Model):
    class Meta:
        abstract = True

    namespace = models.CharField(
        max_length=255,
        help_text=_("Permission namespace (A '.' delimited list of keys"),
    )
    permission = PermissionField(default=PERM_READ)

    def __unicode__(self):
        return f"{self.namespace}: {self.permission}"


class UserPermission(Permission):

    """
    Describes permission for a user
    """

    class Meta:
        verbose_name = _("User Permission")
        verbose_name_plural = _("User Permissions")
        base_manager_name = "objects"

    user = models.ForeignKey(
        get_user_model(), related_name="grainy_permissions", on_delete=models.CASCADE
    )
    objects = PermissionManager()


class GroupPermission(Permission):
    """
    Describes permission for a user group
    """

    class Meta:
        verbose_name = _("Group Permission")
        verbose_name_plural = _("Group Permissions")
        base_manager_name = "objects"

    group = models.ForeignKey(
        Group, related_name="grainy_permissions", on_delete=models.CASCADE
    )
    objects = PermissionManager()
