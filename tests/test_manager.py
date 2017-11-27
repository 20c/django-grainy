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

from grainy.const import (
    PERM_READ,
    PERM_UPDATE,
    PERM_CREATE,
    PERM_DELETE,
)


class TestPermissionManager(UserTestCase):

    EXPECTED_PERMISSIONS_A = PermissionSet({
        "a" : PERM_READ,
        "b" : PERM_READ | PERM_UPDATE
    })

    EXPECTED_PERMISSIONS_A2 = PermissionSet({
        "a" : PERM_READ,
        "b" : PERM_READ | PERM_UPDATE,
        "c" : PERM_READ
    })

    EXPECTED_PERMISSIONS_B = PermissionSet({
        "c" : PERM_READ,
        "d" : PERM_CREATE
    })

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
            PermissionSet({"c" : PERM_READ})
        )
        pset = self.users["user_a"].grainy_permissions.permission_set()
        self.assertEqual(self.EXPECTED_PERMISSIONS_A2.permissions, pset.permissions)

        self.users["user_a"].grainy_permissions.add_permission_set(
            PermissionSet({"c" : PERM_READ}),
            clear=True
        )
        pset = self.users["user_a"].grainy_permissions.permission_set()
        self.assertEqual(PermissionSet({"c": PERM_READ}).permissions, pset.permissions)









