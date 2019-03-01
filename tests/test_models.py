from .util import UserTestCase
from django.db import models
from django_grainy.models import UserPermission, GroupPermission, GrainyHandler
from django_grainy.decorators import grainy_model

from django_grainy_test.models import (
    ModelA,
    ModelB,
    ModelC,
    ModelD,
    ModelX,
    ModelY,
    ModelZ
)

from grainy.const import (
    PERM_READ,
    PERM_UPDATE,
    PERM_CREATE,
    PERM_DELETE
)


class TestGrainyHandler(UserTestCase):

    @classmethod
    def setUpTestData(cls):
        UserTestCase.setUpTestData()

    def test_grainy_model_decorator(self):
        a = ModelA.objects.create(name="A1")
        self.assertEqual(a.Grainy.namespace(a), "django_grainy_test.modela.{}".format(a.id))
        b = ModelB.objects.create(name="B1")
        self.assertEqual(b.Grainy.namespace(b), "something.arbitrary.{}".format(b.id))

        c = ModelC.objects.create(name="C1",b=b)
        self.assertEqual(c.Grainy.namespace(), ModelB.Grainy.namespace())
        self.assertEqual(c.Grainy.namespace(c), "something.arbitrary.2.c.3")


        d = ModelD.objects.create(name="D1")
        self.assertEqual(d.Grainy.namespace(value="parent"), "dynamic.parent")
        self.assertEqual(
            d.Grainy.namespace(d, value="parent", other_value="child"),
            "dynamic.parent.child"
        )

        x = ModelX.objects.create(name="X1")
        self.assertEqual(x.Grainy.namespace(), "x")
        self.assertEqual(x.Grainy.namespace(x), "x.{}".format(x.id))

        y = ModelY.objects.create(name="Y1",x=x)
        self.assertEqual(y.Grainy.namespace(), "custom")
        self.assertEqual(y.Grainy.namespace_instance_template, "x.{instance.x.pk}.custom.{instance.pk}")
        self.assertEqual(y.Grainy.namespace(y), "x.5.custom.6")

        z = ModelZ.objects.create(name="Z1",y=y)
        self.assertEqual(z.Grainy.namespace_instance_template, "x.{instance.y.x.pk}.custom.{instance.y.pk}.z.{instance.pk}")
        self.assertEqual(z.Grainy.namespace(z), "x.5.custom.6.z.7")


    def test_grainy_mixin(self):
        a = ModelA.objects.create(name="A1")
        self.assertEqual(a.grainy_namespace, "django_grainy_test.modela.{}".format(a.id))


