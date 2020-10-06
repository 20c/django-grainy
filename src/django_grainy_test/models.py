# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django_grainy.decorators import grainy_model

from django_grainy.models import GrainyMixin, Permission, PermissionManager

# Create your models here.

"""
These are the models used during the django_grainy
unit tests. There is no need to ever install the "django_grainy_test"
app in your project
"""

class ModelBase(GrainyMixin, models.Model):
    class Meta(object):
        abstract = True

@grainy_model()
class ModelA(ModelBase):
    name = models.CharField(max_length=255)

@grainy_model(namespace="something.arbitrary")
class ModelB(ModelA):
    pass

@grainy_model(
    namespace=ModelB.Grainy.namespace(),
    namespace_instance=u"{namespace}.{instance.b.id}.c.{instance.id}"
)
class ModelC(ModelA):
    b = models.ForeignKey(ModelB, related_name="c", on_delete=models.CASCADE)

@grainy_model(
    namespace=u"dynamic.{value}",
    namespace_instance=u"{namespace}.{other_value}"
)
class ModelD(ModelA):
    pass


@grainy_model(namespace="x")
class ModelX(ModelA):
    pass

@grainy_model(namespace="custom", parent="x")
class ModelY(ModelA):
    x = models.ForeignKey(ModelX, related_name="y", on_delete=models.CASCADE)

@grainy_model(namespace="z", parent="y")
class ModelZ(ModelA):
    y = models.ForeignKey(ModelY, related_name="z", on_delete=models.CASCADE)


class APIKey(models.Model):
    key = models.CharField(max_length=255)

class APIKeyPermission(Permission):
    api_key = models.ForeignKey(APIKey, related_name="grainy_permissions", on_delete=models.CASCADE)
    objects = PermissionManager()

