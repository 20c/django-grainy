import grainy.consT

GRAINY_PERM_CHOICES = [
    #(bitmask flag, verbose name, string flag)
    (grainy.const.PERM_CREATE, _("Create"), "c"),
    (grainy.const.PERM_READ, _("Read"), "r"),
    (grainy.const.PERM_UPDATE, _("Update"), "u"),
    (grainy.const.PERM_DELETE, _("Delete"), "d"),
]
