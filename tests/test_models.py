from django_grainy_test.models import (
    ModelA,
    ModelB,
    ModelC,
    ModelD,
    ModelX,
    ModelY,
    ModelZ,
)

from .util import UserTestCase


class TestGrainyHandler(UserTestCase):
    @classmethod
    def setUpTestData(cls):
        UserTestCase.setUpTestData()

    def test_grainy_model_decorator(self):
        a = ModelA.objects.create(name="A1")
        self.assertEqual(a.Grainy.namespace(a), f"django_grainy_test.modela.{a.id}")
        b = ModelB.objects.create(name="B1")
        self.assertEqual(b.Grainy.namespace(b), f"something.arbitrary.{b.id}")

        c = ModelC.objects.create(name="C1", b=b)
        self.assertEqual(c.Grainy.namespace(), ModelB.Grainy.namespace())
        self.assertEqual(c.Grainy.namespace(c), "something.arbitrary.2.c.3")

        d = ModelD.objects.create(name="D1")
        self.assertEqual(d.Grainy.namespace(value="parent"), "dynamic.parent")
        self.assertEqual(
            d.Grainy.namespace(d, value="parent", other_value="child"),
            "dynamic.parent.child",
        )

        x = ModelX.objects.create(name="X1")
        self.assertEqual(x.Grainy.namespace(), "x")
        self.assertEqual(x.Grainy.namespace(x), f"x.{x.id}")

        y = ModelY.objects.create(name="Y1", x=x)
        self.assertEqual(y.Grainy.namespace(), "custom")
        self.assertEqual(
            y.Grainy.namespace_instance_template,
            "x.{instance.x.pk}.{namespace}.{instance.pk}",
        )
        self.assertEqual(y.Grainy.namespace(y), "x.5.custom.6")

        z = ModelZ.objects.create(name="Z1", y=y)
        self.assertEqual(
            z.Grainy.namespace_instance_template,
            "x.{instance.y.x.pk}.custom.{instance.y.pk}.{namespace}.{instance.pk}",
        )
        self.assertEqual(z.Grainy.namespace(z), "x.5.custom.6.z.7")

    def test_grainy_mixin(self):
        a = ModelA.objects.create(name="A1")
        self.assertEqual(a.grainy_namespace, f"django_grainy_test.modela.{a.id}")
