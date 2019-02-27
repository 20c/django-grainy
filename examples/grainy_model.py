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
class TestModelB(models.Model)
    name = models.CharField(max_length=255)

# initialize grainy permissions for a model
# with manual namespacing for both class
# and instance namespace
@grainy_model(
    # we want the same base namespace as model b
    namespace=TestModelB.Grainy.namespace(),

    # when checking against instances we want to
    # nest inside b
    namespace_instance = u"{namespace}.{instance.b.id}.b.{instance.id}"
)
class TestModelC(models.Model):
    b = models.ForeignKey(TestModelB)


# starting with 1.7 you can also use the `related` argument
# to quickly setup namespace inheritance between related models

@grainy_model(namespace="x")
class ModelX(ModelA):
    pass

# We set related to `x`, to indicate that we want to inherit
# the namespacing from there. It needs to point to ForeignKey or OneToOne
# field on the model that points to a model that is also grainy (ModelX
# in this example)
#
# ModelY will end up with the instance namespace
# "x.(x.pk).custom.(pk)"
@grainy_model(namespace="custom", related="x")
class ModelY(ModelA):
    # field name == grainy `related` value
    x = models.ForeignKey(ModelX, related_name="y", on_delete=models.CASCADE)


# ModelZ will end up with the instance namespace
# "x.(y.x.pk).custom.(y.pk).z.(pk)"
@grainy_model(namespace="z", related="y")
class ModelZ(ModelA):
    # field name == grainy `related` value
    y = models.ForeignKey(ModelY, related_name="z", on_delete=models.CASCADE)
