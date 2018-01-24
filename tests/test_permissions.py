import json

from .util import UserTestCase
from django.test import Client, RequestFactory
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
    detail,
    Detail,
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
        "detail.1" : PERM_READ | PERM_CREATE | PERM_UPDATE | PERM_DELETE,
        "detail_manual.1" : PERM_READ | PERM_CREATE | PERM_UPDATE | PERM_DELETE,
        "detail_manual.GET" : PERM_READ,
        "detail_manual" : PERM_CREATE,
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
                "detail" : "r",
                "detail.1" : "crud",
                JsonView.Grainy.namespace(): "r",
                JsonView.Grainy.namespace("nested_dict.secret"): "r"
            }
        )

        cls.users["user_admin_a"].grainy_permissions.add_permission_set(
            {
                "detail.1" : "crud"
            }
        )

        cls.groups["group_a"].grainy_permissions.add_permission_set(
            cls.GROUP_PERMISSIONS_A
        )


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

        perms = Permissions(self.users["user_admin_a"])
        self.assertTrue(perms.check("x.y.z", PERM_READ))
        self.assertFalse(perms.check("x.y.z", PERM_READ, ignore_grant_all=True))

    def test_permissions_get(self):
        """
        test django.grainy.util.Permissions.get
        """

        perms = Permissions(self.users["user_a"])

        self.assertEqual(perms.get(ModelA), PERM_READ)
        self.assertEqual(perms.get(ModelA, as_string=True), "r")
        self.assertEqual(perms.get(ModelB), PERM_READ | PERM_UPDATE)
        self.assertEqual(perms.get(ModelB, as_string=True), "ru")
        self.assertEqual(perms.get("detail_manual", as_string=True), "c")
        self.assertEqual(perms.get("detail_manual.1", as_string=True, explicit=True), "crud")
        self.assertEqual(perms.get("detail_manual.2", as_string=True, explicit=True), "")
        self.assertEqual(perms.get("detail_manual.2", as_string=True), "c")



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

        ## test function view
        response = self.userclient("user_a").get("/view/")
        self.assertEqual(response.status_code, 200)

        response = self.userclient("user_b").get("/view/")
        self.assertEqual(response.status_code, 403)

        ## test class view
        for method in ["POST", "GET", "PUT", "PATCH", "DELETE"]:
            response = getattr(self.userclient("user_a"), method.lower())("/view_class/")
            self.assertEqual(response.status_code, 200)

            response = getattr(self.userclient("user_b"), method.lower())("/view_class/")
            self.assertEqual(response.status_code, 403)

        # test namespace formatting from request param
        client = self.userclient("user_a")

        response = client.get("/detail/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), "ID 1")

        response = client.get("/detail/2/")
        self.assertEqual(response.status_code, 403)

        for method in ["get","post","delete","put","patch"]:
            response = getattr(client, method)("/detail_class/1/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content.decode("utf-8"), "{} Response 1".format(method.upper()))

            response = getattr(client, method)("/detail_class/2/")
            self.assertEqual(response.status_code, 403)

        # test explicit view

        for username in ["user_c", "user_admin_a"]:

            response = self.userclient(username).get("/detail_explicit/1/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content.decode("utf-8"), "ID 1")

            response = self.userclient(username).get("/detail_explicit/2/")
            self.assertEqual(response.status_code, 403)

            for method in ["get","post","delete","put","patch"]:
                response = getattr(self.userclient(username), method)("/detail_class_explicit/1/")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content.decode("utf-8"), "{} Response 1".format(method.upper()))

                response = getattr(self.userclient(username), method)("/detail_class_explicit/2/")
                self.assertEqual(response.status_code, 403)



        # test class manual view
        response = self.userclient("user_a").get("/detail_class_manual/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), "GET Response 1")

        response = self.userclient("user_a").post("/detail_class_manual/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), "POST Response 1")

        # test class view with request object in namespace
        # formatting
        response = self.userclient("user_a").get("/detail_class_reqfmt/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), "GET Response 1")

        response = self.userclient("user_a").delete("/detail_class_reqfmt/1/")
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

    def test_permissions_instances(self):
        """
        test util.Permissions.instances
        """

        perms_a = Permissions(self.users["user_a"])
        perms_b = Permissions(self.users["user_b"])
        perms_admin = Permissions(self.users["user_admin_a"])

        for i in range(1,4):
            ModelA.objects.create(name="Test {}".format(i))

        # user a should have read to all 3 instances of model a
        # through implicit permissions
        instances = perms_a.instances(ModelA, "r")
        self.assertEqual(len(instances), 3)

        # user as should have read to to 0 instances of model a
        # through explicit permissions
        instances = perms_a.instances(ModelA, "r", explicit=True)
        self.assertEqual(len(instances), 0)

        # add user a permission to first isntance of model a
        # and reload permissions util
        self.users["user_a"].grainy_permissions.add_permission(ModelA.objects.first(), "r")
        perms_a.load(refresh=True)

        # user a should now habe read to 1 instances of model a
        # through explicit permissions
        instances = perms_a.instances(ModelA, "r", explicit=True)
        self.assertEqual(len(instances), 1)

        # user b should not have any
        instances = perms_b.instances(ModelA, "r")
        self.assertEqual(len(instances), 0)

        # deny user a permissions to first instance of model a
        # and reload permissions util
        self.users["user_a"].grainy_permissions.add_permission(ModelA.objects.first(), 0)
        perms_a.load(refresh=True)

        # user a should now have read access to 2 instances of model a
        instances = perms_a.instances(ModelA, "r")
        self.assertEqual(len(instances), 2)

        # admin user should have read to all 3 instances of model a
        # through grant all
        instances = perms_admin.instances(ModelA, "r")
        self.assertEqual(len(instances), 3)

        # admin user should have read to 0 instances of model
        # when ignoring grant all
        instances = perms_admin.instances(ModelA, "r", ignore_grant_all=True)
        self.assertEqual(len(instances), 0)


