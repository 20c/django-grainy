from .util import UserTestCase
from django_grainy.models import UserPermission, GroupPermission
from django_grainy.fields import PermissionField

from grainy.const import (
    PERM_READ,
    PERM_UPDATE,
    PERM_CREATE,
    PERM_DELETE
)

class TestPermissionField(UserTestCase):

    @classmethod
    def setUpTestData(cls):
        UserTestCase.setUpTestData()

    def test_set(self):
        uperm = UserPermission()
        uperm.namespace = "test"
        uperm.user = self.users["user_a"]

        uperm.permission = PERM_READ | PERM_UPDATE
        uperm.full_clean()
        self.assertEqual(uperm.permission, PERM_READ | PERM_UPDATE)

        uperm.permission = "crud"
        uperm.full_clean()
        self.assertEqual(uperm.permission, PERM_READ | PERM_UPDATE | PERM_CREATE | PERM_DELETE)



