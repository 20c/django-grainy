import re
import logging


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from .helpers import (
    django_op_to_flag,
)

from .models import (
    namespace,
)

from .util import (
    Permissions,
)


class GrainyBackend(ModelBackend):

    """
    Authenticate actions using grainy permissions
    """

    def has_module_perms(self, user, obj=None):

        # superusers have access to everything
        if user.is_superuser:
            return True

        return Permissions(user).check(obj, django_op_to_flag("view"))

    def has_perm(self, user, perm, obj=None):

        # superusers have access to everything
        if user.is_superuser:
            return True

        ns = None
        if obj:
            try:
                ns = namespace(obj)
            except TypeError as inst:
                ns = None

        try:
            label, action = tuple(perm.split("."))
            a = re.match("(add|delete|change|view)_(.+)", action)
        except ValueError as inst:
            a = None

        if a:
            flag = django_op_to_flag(a.group(1))
            if not ns:
                ns = "{}.{}".format(label, a.group(2))
        else:
            flag = django_op_to_flag("view")
            if not ns:
                ns = perm

        return Permissions(user).check(ns, flag)
