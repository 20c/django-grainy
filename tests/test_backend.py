from .util import UserTestCase
from django.db import models

from grainy.const import (
    PERM_READ,
    PERM_UPDATE,
    PERM_CREATE,
    PERM_DELETE,
)

from grainy.core import (
    PermissionSet,
)

from django_grainy.backends import GrainyBackend

class TestGrainyBackend(UserTestCase):

    EXPECTED_PERMISSIONS_A = PermissionSet({
        "auth" : PERM_READ,
        "auth.user" : PERM_READ | PERM_UPDATE
    })

    @classmethod
    def setUpTestData(cls):
        UserTestCase.setUpTestData()

        cls.users["user_a"].grainy_permissions.add_permission_set(
            cls.EXPECTED_PERMISSIONS_A
        )


    def test_has_module_perms(self):
        user = self.users["user_a"]
        backend = GrainyBackend()
        self.assertEqual(backend.has_module_perms(user, "auth"), True)
        self.assertEqual(backend.has_module_perms(user, "other"), False)

    def test_has_perm(self):
        user = self.users["user_a"]
        backend = GrainyBackend()
        self.assertEqual(backend.has_perm(user, "auth.view_user"), True)
        self.assertEqual(backend.has_perm(user, "auth.change_user"), True)
        self.assertEqual(backend.has_perm(user, "auth.add_user"), False)
        self.assertEqual(backend.has_perm(user, "auth.delete_user"), False)

