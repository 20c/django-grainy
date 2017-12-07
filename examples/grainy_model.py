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
