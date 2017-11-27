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

    @classmethod
    def setUpTestData(cls):
        UserTestCase.setUpTestData()

        cls.users["user_a"].grainy_permissions.add_permission_set(
            cls.EXPECTED_PERMISSIONS_A
        )


    def test_permission_set_from_query(self):
        pset = self.users["user_a"].grainy_permissions.permission_set()
        self.assertEqual(self.EXPECTED_PERMISSIONS_A.permissions, pset.permissions)
