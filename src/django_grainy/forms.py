from django import forms

from .conf import PERM_CHOICES_FOR_FIELD
from .fields import PermissionFormField
from .models import GroupPermission, UserPermission


class BitmaskSelect(forms.widgets.CheckboxSelectMultiple):
    template_name = "django_grainy/forms/widgets/bitmask_select.html"


class UserPermissionForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        fields = ["namespace", "permission"]

    permission = PermissionFormField(
        widget=BitmaskSelect(choices=PERM_CHOICES_FOR_FIELD)
    )


class GroupPermissionForm(UserPermissionForm):
    class Meta:
        model = GroupPermission
        fields = ["namespace", "permission"]
