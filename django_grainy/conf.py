from django.conf import settings

from .const import PERM_CHOICES_CRUD

PERM_CHOICES = getattr(settings, "GRAINY_PERM_CHOICES", PERM_CHOICES_CRUD)
PERM_CHOICES_FOR_FIELD = [(n,v) for n,v,c in PERM_CHOICES]

# if True, the default django forms for adding / editing permissions
# will be removed.
ADMIN_REMOVE_DEFAULT_FORMS = getattr(
    settings, "GRAINY_ADMIN_REMOVE_DEFAULT_FORMS", True
)
