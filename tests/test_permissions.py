from .util import UserTestCase
from django.db import models
from django_grainy.models import (
    UserPermission,
    GroupPermission,
    GrainyHandler,
    PermissionSet
)
from django_grainy.decorators import grainy_model

from django_grainy_test.models import (
    ModelA,
    ModelB
)

from django_grainy.util import (
    namespace,
    Permissions
)

from grainy.const import (
    PERM_READ,
    PERM_UPDATE,
    PERM_CREATE,
    PERM_DELETE,
)

class TestPermissions(UserTestCase):

    EXPECTED_PERMISSIONS_A = PermissionSet({
        ModelA.Grainy.namespace() : PERM_READ,
        ModelB.Grainy.namespace() : PERM_READ | PERM_UPDATE
    })


    @classmethod
    def setUpTestData(cls):
        UserTestCase.setUpTestData()

        cls.users["user_a"].grainy_permissions.add_permission_set(
            cls.EXPECTED_PERMISSIONS_A
        )

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








