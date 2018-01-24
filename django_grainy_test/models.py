# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django_grainy.decorators import grainy_model

# Create your models here.

"""
These are the models used during the django_grainy
unit tests. There is no need to ever install the "django_grainy_test"
app in your project
"""

class ModelBase(models.Model):
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
    b = models.ForeignKey(ModelB, related_name="c")

@grainy_model(
    namespace=u"dynamic.{value}",
    namespace_instance=u"{namespace}.{other_value}"
)
class ModelD(ModelA):
    pass
