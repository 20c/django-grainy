import re
from typing import Any, Optional

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .helpers import django_op_to_flag
from .models import namespace
from .util import Permissions


class GrainyBackend(ModelBackend):

    """
    Authenticate actions using grainy permissions
    """

    def has_module_perms(self, user: User, obj: str = None) -> bool:

        # superusers have access to everything
        if user.is_superuser:
            return True

        return Permissions(user).check(obj, django_op_to_flag("view"))

    def has_perm(self, user: User, perm: str, obj: Optional[Any] = None) -> bool:

        # superusers have access to everything
        if user.is_superuser:
            return True

        ns = None
        if obj:
            try:
                ns = namespace(obj)
            except TypeError:
                ns = None

        try:
            label, action = tuple(perm.split("."))
            a = re.match("(add|delete|change|view)_(.+)", action)
        except ValueError:
            a = None

        if a:
            flag = django_op_to_flag(a.group(1))
            if not ns:
                ns = f"{label}.{a.group(2)}"
        else:
            flag = django_op_to_flag("view")
            if not ns:
                ns = perm

        return Permissions(user).check(ns, flag)
