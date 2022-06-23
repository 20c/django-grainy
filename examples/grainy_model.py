from django.db import models
from grainy.decorators import grainy_model


# initialize grainy permissions for a model
# with automatic namespacing
@grainy_model()
class TestModelA(models.Model):
    name = models.CharField(max_length=255)


# initialize grainy permissions for a model
# with manual namespacing
@grainy_model(namespace="a.b.c")
class TestModelB(models.Model):
    name = models.CharField(max_length=255)


# initialize grainy permissions for a model
# with manual namespacing for both class
# and instance namespace
@grainy_model(
    # we want the same base namespace as model b
    namespace=TestModelB.Grainy.namespace(),
    # when checking against instances we want to
    # nest inside b
    namespace_instance="{namespace}.{instance.b.id}.b.{instance.id}",
)
class TestModelC(models.Model):
    b = models.ForeignKey(TestModelB)
