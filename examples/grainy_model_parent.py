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
