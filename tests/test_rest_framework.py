from rest_framework.test import APIClient
from django.test import RequestFactory
from .util import UserTestCase

from grainy.const import (
    PERM_READ
)

from grainy.core import (
    PermissionSet,
)

from django_grainy_test.views import (
    ModelAViewSet,
)

from django_grainy_test.models import (
    ModelA,
)

class TestGrainyViewSet(UserTestCase):

    @classmethod
    def setUpTestData(cls):
        UserTestCase.setUpTestData()

        cls.users["user_a"].grainy_permissions.add_permission_set(
            PermissionSet({
                "api" : PERM_READ,
                "api.a.*.nested_dict.secret": PERM_READ
            })
        )

        cls.users["user_b"].grainy_permissions.add_permission_set(
            PermissionSet({
                "api" : PERM_READ
            })
        )

        ModelA.objects.create(name="Test1")



    def test_grainy_viewset(self):
        client = APIClient()
        client.force_authenticate(user=self.users["user_a"])
        response = client.get("/a/?format=json", follow=True)

        self.assertEqual(response.data, [
            {
                "name": "Test1",
                "id":1,
                "nested_dict": {
                    "secret" : {
                        "hidden" : "data"
                    },
                    "something": "public"
                }
            }
        ])

        client = APIClient()
        client.force_authenticate(user=self.users["user_b"])
        response = client.get("/a/?format=json", follow=True)

        self.assertEqual(response.data, [
            {
                "name": "Test1",
                "id":1,
                "nested_dict": {
                    "something": "public"
                }
            }
        ])

