from django.conf import settings

from .const import PERM_CHOICES_CRUD

PERM_CHOICES = getattr(settings, "GRAINY_PERM_CHOICES", PERM_CHOICES_CRUD)
