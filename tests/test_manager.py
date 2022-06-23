from django.db import models
from grainy.const import PERM_CREATE, PERM_DELETE, PERM_READ, PERM_UPDATE

from django_grainy.decorators import grainy_model
from django_grainy.handlers import GrainyHandler
from django_grainy.models import GroupPermission, PermissionSet, UserPermission
from django_grainy_test.models import ModelA, ModelB

from .util import UserTestCase


class TestPermissionManager(UserTestCase):

    EXPECTED_PERMISSIONS_A = PermissionSet(
        {"a": PERM_READ, "b": PERM_READ | PERM_UPDATE}
    )

    EXPECTED_PERMISSIONS_A2 = PermissionSet(
        {"a": PERM_READ, "b": PERM_READ | PERM_UPDATE, "c": PERM_READ}
    )

    EXPECTED_PERMISSIONS_B = PermissionSet({"c": PERM_READ, "d": PERM_CREATE})

    EXPECTED_PERMISSIONS_C = PermissionSet(
        {
            ModelA.Grainy.namespace(): PERM_READ
            | PERM_UPDATE
            | PERM_CREATE
            | PERM_DELETE,
            ModelB.Grainy.namespace(): PERM_READ,
        }
    )

    @classmethod
    def setUpTestData(cls):
        UserTestCase.setUpTestData()

        cls.users["user_a"].grainy_permissions.add_permission_set(
            cls.EXPECTED_PERMISSIONS_A
        )
        cls.users["user_b"].grainy_permissions.add_permission_set(
            cls.EXPECTED_PERMISSIONS_B
        )

    def test_permission_set_from_query(self):
        pset = self.users["user_a"].grainy_permissions.permission_set()
        self.assertEqual(self.EXPECTED_PERMISSIONS_A.permissions, pset.permissions)

        pset = self.users["user_b"].grainy_permissions.permission_set()
        self.assertEqual(self.EXPECTED_PERMISSIONS_B.permissions, pset.permissions)

    def test_permission_set_upates(self):
        self.users["user_a"].grainy_permissions.add_permission_set(
            PermissionSet({"c": PERM_READ})
        )
        pset = self.users["user_a"].grainy_permissions.permission_set()
        self.assertEqual(self.EXPECTED_PERMISSIONS_A2.permissions, pset.permissions)

    def test_add_permission(self):
        self.users["user_c"].grainy_permissions.add_permission(ModelA, "crud")
        self.users["user_c"].grainy_permissions.add_permission(ModelB, PERM_READ)
        pset = self.users["user_c"].grainy_permissions.permission_set()
        self.assertEqual(self.EXPECTED_PERMISSIONS_C.permissions, pset.permissions)

    def test_del_permission(self):
        self.users["user_b"].grainy_permissions.add_permission(ModelA, "crud")
        self.users["user_c"].grainy_permissions.add_permission(ModelA, "crud")
        self.users["user_c"].grainy_permissions.add_permission(ModelB, PERM_READ)
        pset = self.users["user_c"].grainy_permissions.permission_set()
        self.assertEqual(self.EXPECTED_PERMISSIONS_C.permissions, pset.permissions)

        self.users["user_c"].grainy_permissions.delete_permission(ModelA)

        pset = self.users["user_c"].grainy_permissions.permission_set()
        self.assertNotEqual(self.EXPECTED_PERMISSIONS_C.permissions, pset.permissions)
        self.assertEqual(pset.check(ModelB.Grainy.namespace(), PERM_READ), True)

        pset = self.users["user_b"].grainy_permissions.permission_set()
        self.assertEqual(pset.check(ModelA.Grainy.namespace(), PERM_CREATE), True)
