from django import forms

from .models import (
    UserPermission,
    GroupPermission
)
from .conf import (
    PERM_CHOICES_FOR_FIELD,
)
from .fields import (
    PermissionFormField,
)

class BitmaskSelect(forms.widgets.CheckboxSelectMultiple):
    template_name = "django_grainy/forms/widgets/bitmask_select.html";

class UserPermissionForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        fields = ["namespace", "permission"]
        widgets = {
            "permission" : BitmaskSelect(choices=PERM_CHOICES_FOR_FIELD)
        }
    permission = PermissionFormField(widget=BitmaskSelect(choices=PERM_CHOICES_FOR_FIELD))
