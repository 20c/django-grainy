from rest_framework.test import APIClient
from django.test import RequestFactory
from .util import UserTestCase

from grainy.const import (
    PERM_READ,
    PERM_CREATE,
    PERM_UPDATE,
    PERM_DELETE
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
                "api" : PERM_READ | PERM_CREATE | PERM_UPDATE | PERM_DELETE,
                "api.a.*.nested_dict.secret": PERM_READ
            })
        )

        cls.users["user_b"].grainy_permissions.add_permission_set(
            PermissionSet({
                "api" : PERM_READ,
                "api.a_x" : PERM_READ
            })
        )

        ModelA.objects.create(name="Test1")


    def test_grainy_viewset_gate(self):

        client_a = APIClient()
        client_a.force_authenticate(user=self.users["user_a"])

        r = client_a.post("/a/", {"name":"bla"})
        self.assertEqual(r.status_code, 201)
        r = client_a.put("/a/2/", {"name":"bla2"})
        self.assertEqual(r.status_code, 200)
        r = client_a.patch("/a/2/", {"name":"bla3"})
        self.assertEqual(r.status_code, 200)
        r = client_a.delete("/a/2/", follow=True)
        self.assertEqual(r.status_code, 404)

        r = client_a.get("/a_x/1/")
        self.assertEqual(r.status_code, 403)
        r = client_a.delete("/a_x/1/")
        self.assertEqual(r.status_code, 403)


        client_b = APIClient()
        client_b.force_authenticate(user=self.users["user_b"])

        r = client_b.post("/a/", {"name":"bla"})
        self.assertEqual(r.status_code, 403)
        r = client_b.put("/a/1/", {"name":"bla2"})
        self.assertEqual(r.status_code, 403)
        r = client_b.patch("/a/1/", {"name":"bla3"})
        self.assertEqual(r.status_code, 403)
        r = client_b.delete("/a/1/", follow=True)
        self.assertEqual(r.status_code, 403)

        r = client_b.get("/a_x/1/")
        self.assertEqual(r.status_code, 200)
        r = client_b.delete("/a_x/1/")
        self.assertEqual(r.status_code, 403)





    def test_grainy_viewset_list(self):
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

    def test_grainy_viewset_retrieve(self):
        client = APIClient()
        client.force_authenticate(user=self.users["user_a"])
        response = client.get("/a/1/?format=json", follow=True)

        self.assertEqual(response.data, 
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
        )

        client = APIClient()
        client.force_authenticate(user=self.users["user_b"])
        response = client.get("/a/1/?format=json", follow=True)

        self.assertEqual(response.data,
            {
                "name": "Test1",
                "id":1,
                "nested_dict": {
                    "something": "public"
                }
            }
        )

