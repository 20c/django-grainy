import json

from .util import UserTestCase
from django.test import RequestFactory
from django.test.utils import override_settings
from django.db import models
from django.contrib.auth.models import AnonymousUser


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

from django_grainy_test.views import (
    View,
    view,
    JsonView
)

from django_grainy.util import (
    namespace,
    int_flags,
    str_flags,
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
        ModelB.Grainy.namespace() : PERM_READ | PERM_UPDATE,
        view.Grainy.namespace() : PERM_READ,
        View.Grainy.namespace() : PERM_READ | PERM_CREATE | PERM_UPDATE | PERM_DELETE,
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

        cls.users["user_b"].grainy_permissions.add_permission_set(
            {
                "x.y.z" : "r"
            }
        )

        cls.users["user_c"].grainy_permissions.add_permission_set(
            {
                JsonView.Grainy.namespace(): "r",
                JsonView.Grainy.namespace("nested_dict.secret"): "r"
            }
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

        perms = Permissions(self.users["user_b"])
        self.assertTrue(perms.check("x.y.z", PERM_READ))
        self.assertFalse(perms.check("x.y.z", PERM_UPDATE))


    def test_anonymous_permissions(self):
        user = AnonymousUser()
        perms = Permissions(user)
        self.assertTrue(perms.check("a.b.c", PERM_READ))
        self.assertTrue(perms.check("a.b.c.d", PERM_UPDATE | PERM_READ))
        self.assertFalse(perms.check("x.y.z", PERM_READ))


    def test_grainy_view(self):
        """
        test grainy_view decorator
        """

        factory = RequestFactory()
        ## test function view

        request = factory.get("/view/")
        request.user = self.users["user_a"]
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = factory.get("/view/")
        request.user = self.users["user_b"]
        response = view(request)
        self.assertEqual(response.status_code, 403)

        ## test class view

        for method in ["POST", "GET", "PUT", "PATCH", "DELETE"]:
            request = getattr(factory, method.lower())("/view_class/")
            request.user = self.users["user_a"]
            response = View().dispatch(request)
            self.assertEqual(response.status_code, 200)

            request = getattr(factory, method.lower())("/view_class/")
            request.user = self.users["user_b"]
            response = View().dispatch(request)
            self.assertEqual(response.status_code, 403)



    def test_grainy_json_view(self):
        """
        test grainy_json_view decorator
        """

        factory = RequestFactory()

        request = factory.get("/view_class_json/")
        request.user = self.users["user_a"]
        response = JsonView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            json.loads(response.content.decode("utf-8")),
            {"hello": "world", "nested_dict": {"public": "something"}}
        )

        request = factory.get("/view_class_json/")
        request.user = self.users["user_c"]
        response = JsonView().dispatch(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode("utf-8")),
            {"hello": "world", "nested_dict": {"secret": "hidden", "public": "something"}}
        )
