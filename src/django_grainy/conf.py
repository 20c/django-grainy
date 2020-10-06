import grainy.const
from django.conf import settings
from .const import PERM_CHOICES_CRUD

DJANGO_OP_TO_FLAG = getattr(
    settings,
    "GRAINY_DJANGO_OP_TO_FLAG",
    {
        "add": grainy.const.PERM_CREATE,
        "delete": grainy.const.PERM_DELETE,
        "change": grainy.const.PERM_UPDATE,
        "view": grainy.const.PERM_READ,
    },
)

REQUEST_METHOD_TO_FLAG = getattr(
    settings,
    "GRAINY_REQUEST_METHOD_TO_FLAG",
    {
        "HEAD": grainy.const.PERM_READ,
        "OPTIONS": grainy.const.PERM_READ,
        "GET": grainy.const.PERM_READ,
        "PUT": grainy.const.PERM_UPDATE,
        "PATCH": grainy.const.PERM_UPDATE,
        "POST": grainy.const.PERM_CREATE,
        "DELETE": grainy.const.PERM_DELETE,
    },
)

ANONYMOUS_PERMS = getattr(settings, "GRAINY_ANONYMOUS_PERMS", {})

PERM_CHOICES = getattr(settings, "GRAINY_PERM_CHOICES", PERM_CHOICES_CRUD)
PERM_CHOICES_FOR_FIELD = [(n, v) for n, v, c in PERM_CHOICES]

# if True, the default django forms for adding / editing permissions
# will be removed.
ADMIN_REMOVE_DEFAULT_FORMS = getattr(
    settings, "GRAINY_ADMIN_REMOVE_DEFAULT_FORMS", True
)
