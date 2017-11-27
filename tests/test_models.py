from .util import UserTestCase
from django.db import models
from django_grainy.models import UserPermission, GroupPermission, GrainyHandler
from django_grainy.decorators import grainy_model

from django_grainy_test.models import (
    TestModelA,
    TestModelB
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
        a = TestModelA.objects.create(name="A1")
        self.assertEqual(a.Grainy.namespace(a), "django_grainy_test.testmodela.{}".format(a.id))
        b = TestModelB.objects.create(name="B1")
        self.assertEqual(b.Grainy.namespace(b), "something.arbitrary.{}".format(b.id))

