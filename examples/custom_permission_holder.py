from django.db import models

from django_grainy.models import Permission, PermissionManager


class APIKey(models.Model):
    key = models.CharField(max_length=255)


class APIKeyPermission(Permission):
    # The `grainy_permissions` related name is important
    # so that we can pass instances of this model to
    # util.Permissions
    api_key = models.ForeignKey(
        APIKey, related_name="grainy_permissions", on_delete=models.CASCADE
    )

    # use the augmented object manager for permission handling
    objects = PermissionManager()


from django_grainy.util import Permissions

api_key = APIKey.objects.create(key="test")
api_key.grainy_permissions.add_permission("a.b.c", "r")

perms = Permissions(api_key)
assert api_key.check("a.b.c", "r")
