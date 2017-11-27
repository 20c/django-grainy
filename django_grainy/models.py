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
    class Meta(object):
        verbose_name = _("User Permission")
        verbose_name_plural = _("User Permissions")

    user = models.ForeignKey(get_user_model(), related_name="grainy_permissions", on_delete=models.CASCADE)

class GroupPermission(Permission):
    class Meta(object):
        verbose_name = _("Group Permission")
        verbose_name_plural = _("Group Permissions")

    group = models.ForeignKey(Group, related_name="grainy_permissions", on_delete=models.CASCADE)


class GrainyHandler(object):

    model = None

    @classmethod
    def namespace_instance(cls, instance):
        return u"{}.{}".format(
            cls.namespace_model(),
            instance.id
        ).lower()

    @classmethod
    def namespace_model(cls):
        return u"{}.{}".format(
            cls.model._meta.app_label,
            cls.model._meta.object_name
        ).lower()

    @classmethod
    def namespace(cls, instance=None):
        if instance:
            return cls.namespace_instance(instance)
        return cls.namespace_model()

