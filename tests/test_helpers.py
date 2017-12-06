from unittest import TestCase
from grainy.core import (
    Namespace,
)
from django_grainy.helpers import (
    dict_get_namespace,
)

class TestHelpers(TestCase):
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

