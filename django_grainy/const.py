import grainy.const
from django.utils.translation import ugettext_lazy as _

PERM_CHOICES_RW = [
    (grainy.const.PERM_READ, _("Read"), "r"),
    (grainy.const.PERM_WRITE, _("Write"), "w"),
]

PERM_CHOICES_CRUD = [
    (grainy.const.PERM_CREATE, _("Create"), "c"),
    (grainy.const.PERM_READ, _("Read"), "r"),
    (grainy.const.PERM_UPDATE, _("Update"), "u"),
    (grainy.const.PERM_DELETE, _("Delete"), "d"),
]
