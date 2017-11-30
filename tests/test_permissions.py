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
    convert_flags,
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

    GROUP_PERMISSIONS_A = PermissionSet({
        "secret.group" : PERM_READ
    })


    @classmethod
    def setUpTestData(cls):
        UserTestCase.setUpTestData()

        cls.users["user_a"].grainy_permissions.add_permission_set(
            cls.EXPECTED_PERMISSIONS_A
        )

        cls.groups["group_a"].grainy_permissions.add_permission_set(
            cls.GROUP_PERMISSIONS_A
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

    def test_convert_flags(self):
        """
        test django_grainy.util.convert_flags
        """

        self.assertEqual(convert_flags("c"), PERM_CREATE)
        self.assertEqual(convert_flags("cr"), PERM_CREATE | PERM_READ)
        self.assertEqual(convert_flags("cru"), PERM_CREATE | PERM_READ | PERM_UPDATE)
        self.assertEqual(convert_flags("crud"), PERM_CREATE | PERM_READ | PERM_UPDATE | PERM_DELETE)
        self.assertEqual(convert_flags("xyz"), 0)
        self.assertEqual(convert_flags(None), 0)

        self.assertEqual(convert_flags(convert_flags("c")), PERM_CREATE)
        self.assertEqual(convert_flags(convert_flags("cr")), PERM_CREATE | PERM_READ)
        self.assertEqual(convert_flags(convert_flags("cru")), PERM_CREATE | PERM_READ | PERM_UPDATE)
        self.assertEqual(convert_flags(convert_flags("crud")), PERM_CREATE | PERM_READ | PERM_UPDATE | PERM_DELETE)

        with self.assertRaises(TypeError):
            convert_flags(object())


    def test_permissions_init(self):
        """
        test django.grainy.util.Permissions.__init__
        """
        user = self.users["user_a"]
        group = self.groups["group_a"]

        self.assertEqual(Permissions(user).obj, user)
        self.assertEqual(Permissions(group).obj, group)
        with self.assertRaises(ValueError):
            Permissions(object())

    def test_permissions_check(self):
        """
        test django.grainy.util.Permissions.check
        """
        user = self.users["user_a"]

        perms = Permissions(user)
        self.assertTrue(perms.check(ModelA, PERM_READ))
        self.assertFalse(perms.check(ModelA, PERM_UPDATE))
        self.assertTrue(perms.check(ModelB, PERM_READ))
        self.assertTrue(perms.check(ModelB, PERM_UPDATE))
        self.assertTrue(perms.check(ModelA(), PERM_READ))
        self.assertFalse(perms.check(ModelA(), PERM_UPDATE))
        self.assertTrue(perms.check(ModelB(), PERM_READ))
        self.assertTrue(perms.check(ModelB(), PERM_UPDATE))
        self.assertTrue(perms.check("secret.group", PERM_READ))
        self.assertFalse(perms.check("secret", PERM_READ))







