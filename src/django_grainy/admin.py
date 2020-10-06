from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .conf import ADMIN_REMOVE_DEFAULT_FORMS
from .models import UserPermission, GroupPermission
from .forms import UserPermissionForm, GroupPermissionForm

# Register your models here.


class UserPermissionInlineAdmin(admin.TabularInline):
    model = UserPermission
    form = UserPermissionForm
    extra = 1
    ordering = ("namespace",)


class GroupPermissionInlineAdmin(admin.TabularInline):
    model = GroupPermission
    form = GroupPermissionForm
    extra = 1
    ordering = ("namespace",)


## INIT

admin.site.unregister(get_user_model())
admin.site.unregister(Group)

_fieldsets = UserAdmin.fieldsets
for name, info in _fieldsets:
    if ADMIN_REMOVE_DEFAULT_FORMS and "user_permissions" in info.get("fields", []):
        lst = list(info.get("fields"))
        lst.remove("user_permissions")
        info["fields"] = lst


@admin.register(get_user_model())
class GrainyUserAdmin(UserAdmin):
    fieldsets = _fieldsets
    inlines = UserAdmin.inlines + [UserPermissionInlineAdmin]


_exclude = []
if ADMIN_REMOVE_DEFAULT_FORMS:
    _exclude.append("permissions")


@admin.register(Group)
class GrainyGroupAdmin(GroupAdmin):
    inlines = GroupAdmin.inlines + [GroupPermissionInlineAdmin]
    exclude = _exclude
