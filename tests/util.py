from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client, TestCase


class UserTestCase(TestCase):
    setup_users = ["user_a", "user_b", "user_c"]
    setup_admins = ["user_admin_a"]
    setup_groups = {"group_a": ["user_a"], "group_b": ["user_b"], "group_c": ["user_c"]}

    @classmethod
    def setUpTestData(cls):
        # create users
        cls.users = {
            k: get_user_model().objects.create_user(k, f"{k}@example.com", password=k)
            for k in cls.setup_users
        }

        # create admin users
        cls.users.update(
            {
                k: get_user_model().objects.create_user(
                    k,
                    f"{k}@example.com",
                    password=k,
                    is_staff=True,
                    is_superuser=True,
                )
                for k in cls.setup_admins
            }
        )

        # create usergroups
        cls.groups = {k: Group.objects.create(name=k) for k in cls.setup_groups}

        # add users to groups
        for group in list(cls.groups.values()):
            for username in cls.setup_groups.get(group.name):
                group.user_set.add(cls.users.get(username))

    def userclient(self, username):
        client = Client()
        client.login(username=username, password=username)
        return client
