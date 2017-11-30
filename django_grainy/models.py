# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from grainy.const import PERM_READ
from grainy.core import PermissionSet

from .fields import PermissionField
from .conf import PERM_CHOICES

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

    def add_permission_set(self, pset, clear=False):
        """
        Add all permissions specified in a PermissionSet

        Arguments:
            - pset <grainy.PermissionSet>

        Keyword Arguments:
            - clear <bool>: if true, clear all existing permissions before
                adding the new set.
        """

        if clear:
            _pset = PermissionSet()
        else:
            _pset = self.permission_set()

        self.get_queryset().all().delete()

        for namespace, permission in pset.permissions.items():
            _pset[namespace] = permission

        for namespace, permission in _pset.permissions.items():
            self.create(namespace=namespace, permission=permission.value)

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
    class Meta(object):
        abstract = True

    namespace = models.CharField(
        max_length=255,
        help_text=_("Permission namespace (A '.' delimited list of keys")
    )
    permission = PermissionField(
        default=PERM_READ
    )

    def __unicode__(self):
        return u"{}: {}".format(self.namespace, self.permission)

class UserPermission(Permission):

    """
    Describes permission for a user
    """
    class Meta(object):
        verbose_name = _("User Permission")
        verbose_name_plural = _("User Permissions")
        base_manager_name = "objects"

    user = models.ForeignKey(get_user_model(), related_name="grainy_permissions", on_delete=models.CASCADE)
    objects = PermissionManager()

class GroupPermission(Permission):
    """
    Describes permission for a user group
    """
    class Meta(object):
        verbose_name = _("Group Permission")
        verbose_name_plural = _("Group Permissions")
        base_manager_name = "objects"

    group = models.ForeignKey(Group, related_name="grainy_permissions", on_delete=models.CASCADE)
    objects = PermissionManager()


class GrainyHandler(object):

    """
    The base class to use for the Grainy Meta class to put inside
    Models that you want to use grainy permissions on
    """

    # the model handled
    model = None

    @classmethod
    def namespace_instance(cls, instance):
        """
        Returns the permissioning namespace for the model instance
        passed.

        Arguments:
            - instance (models.Model): model instance

        Returns:
            - unicode
        """
        return u"{}.{}".format(
            cls.namespace_model(),
            instance.id
        ).lower()

    @classmethod
    def namespace_model(cls):
        """
        Returns the permissioning namespace for the model specified
        in cls.model

        Returns:
            - unicode
        """
        return u"{}.{}".format(
            cls.model._meta.app_label,
            cls.model._meta.object_name
        ).lower()

    @classmethod
    def namespace(cls, instance=None):
        """
        Returns the permissioning namespace of the model class mangaged
        by this handler, or an instance of said model if it is specified.

        Keyword Arguments:
            - instance <models.Model>: model instance, if specified 
                the permissioning namespace returned will be fore this instance.

        Returns:
            - unicode
        """
        if instance:
            return cls.namespace_instance(instance)
        return cls.namespace_model()

