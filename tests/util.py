from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class UserTestCase(TestCase):
    setup_users = ["user_a", "user_b", "user_c"]
    setup_groups = {
        "group_a" : ["user_a"],
        "group_b" : ["user_b"],
        "group_c" : ["user_c"]
    }
    @classmethod
    def setUpTestData(cls):
        # create users
        cls.users = dict([
            (k, get_user_model().objects.create_user(k, "{}@example.com".format(k), k))
            for k in cls.setup_users
        ])

        # create usergroups
        cls.groups = dict([
            (k, Group.objects.create(name=k)) for k in cls.setup_groups
        ])

        # add users to groups
        for group in cls.groups.values():
            for username in cls.setup_groups.get(group.name):
                group.user_set.add(cls.users.get(username))



