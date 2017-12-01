# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth import get_user_model

from .conf import ADMIN_REMOVE_DEFAULT_FORMS
from .models import (
    UserPermission,
    GroupPermission
)
from .forms import (
    UserPermissionForm
)

# Register your models here.

class UserPermissionInlineAdmin(admin.TabularInline):
    model = UserPermission
    form = UserPermissionForm
    extra = 1

## INIT

def init_grainy_admin():
    admin.site.unregister(get_user_model())
    _fieldsets = UserAdmin.fieldsets
    for name, info in _fieldsets:
        if ADMIN_REMOVE_DEFAULT_FORMS and "user_permissions" in info.get("fields",[]):
            lst = list(info.get("fields"))
            lst.remove("user_permissions")
            info["fields"] = lst

    @admin.register(get_user_model())
    class GrainyUserAdmin(UserAdmin):
        fieldsets = _fieldsets
        inlines = UserAdmin.inlines + [UserPermissionInlineAdmin]

init_grainy_admin()
