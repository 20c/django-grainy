from unittest import TestCase
from django.test import RequestFactory
from grainy.core import (
    Namespace,
)
from grainy.const import (
    PERM_READ,
    PERM_DELETE,
    PERM_UPDATE,
    PERM_CREATE
)
from django_grainy.helpers import (
    namespace,
    int_flags,
    str_flags,
    dict_get_namespace,
    request_to_flag,
)

from django_grainy_test.models import(
    ModelA,
    ModelD
)

class TestHelpers(TestCase):

    def test_namespace(self):
        """
        test django_grainy.util.namespace
        """

        self.assertEqual(namespace(ModelA), "django_grainy_test.modela")
        self.assertEqual(namespace(ModelA()), "django_grainy_test.modela.none")
        self.assertEqual(namespace("a.b.c"), "a.b.c")
        self.assertEqual(namespace(None), "")
        with self.assertRaises(TypeError):
            namespace(object())

        self.assertEqual(namespace( (ModelA, "name") ), "django_grainy_test.modela.name")
        self.assertEqual(namespace( (ModelA(), "name") ), "django_grainy_test.modela.none.name")

        self.assertEqual(namespace(ModelD, value="parent"), "dynamic.parent")
        self.assertEqual(
            namespace(ModelD(), value="parent", other_value="child"),
            "dynamic.parent.child"
        )


    def test_request_to_flag(self):
        """
        test django_grainy.helpers.request_to_flag
        test django_grainy.helpers.request_method_to_flag
        """
        factory = RequestFactory()

        self.assertEqual(request_to_flag(factory.get("/view_class")), PERM_READ)
        self.assertEqual(request_to_flag(factory.put("/view_class")), PERM_UPDATE)
        self.assertEqual(request_to_flag(factory.post("/view_class")), PERM_CREATE)
        self.assertEqual(request_to_flag(factory.patch("/view_class")), PERM_UPDATE)
        self.assertEqual(request_to_flag(factory.delete("/view_class")), PERM_DELETE)


    def test_dict_get_namespace(self):
        namespace = Namespace("a.b.c")
        self.assertEqual(
            dict_get_namespace({"a":{"b":{"c":123}}}, namespace),
            123
        )
        with self.assertRaises(KeyError) as inst:
            self.assertEqual(
                dict_get_namespace({}, namespace),
                123
            )

    def test_int_flags(self):
        """
        test django_grainy.util.int_flags
        """

        self.assertEqual(int_flags("c"), PERM_CREATE)
        self.assertEqual(int_flags("cr"), PERM_CREATE | PERM_READ)
        self.assertEqual(int_flags("cru"), PERM_CREATE | PERM_READ | PERM_UPDATE)
        self.assertEqual(int_flags("crud"), PERM_CREATE | PERM_READ | PERM_UPDATE | PERM_DELETE)
        self.assertEqual(int_flags("xyz"), 0)
        self.assertEqual(int_flags(None), 0)

        self.assertEqual(int_flags(int_flags("c")), PERM_CREATE)
        self.assertEqual(int_flags(int_flags("cr")), PERM_CREATE | PERM_READ)
        self.assertEqual(int_flags(int_flags("cru")), PERM_CREATE | PERM_READ | PERM_UPDATE)
        self.assertEqual(int_flags(int_flags("crud")), PERM_CREATE | PERM_READ | PERM_UPDATE | PERM_DELETE)

        with self.assertRaises(TypeError):
            int_flags(object())

    def test_str_flags(self):
        """
        test django.grainy.util.str_flags
        """

        self.assertEqual(str_flags(PERM_READ), "r")
        self.assertEqual(str_flags(PERM_READ | PERM_UPDATE), "ru")
        self.assertEqual(str_flags(PERM_READ | PERM_CREATE), "cr")
        self.assertEqual(str_flags(PERM_READ | PERM_DELETE), "rd")



