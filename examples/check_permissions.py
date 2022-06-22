import grainy.const

from django_grainy.util import Permissions

user.grainy_permissions.add_permission_set({"a.b.c": "r"})

# we use the Permissions() wrapper as that allows
# us to do repeated permission checks for a user or group
# without having requery permissions for each check

perms = Permissions(user)

perms.check("a.b.c", grainy.const.PERM_READ)  # True
perms.check("a.b.c.d", grainy.const.PERM_READ)  # True
perms.check("a.b.c.d", grainy.const.PERM_READ | grainy.const.PERM_UPDATE)  # False
perms.check("z.y.x", grainy.const.PERM_READ)  # False
perms.check("a.b.c", "r")  # True
perms.check("a.b.c.d", "r")  # True
perms.check("a.b.c.d", "ru")  # False
perms.check("x.y.z", "r")  # False

# The `explicit` option allows us to require that excplicit
# permissions need to exist for a check to succeed, meaning
# having permissions to `a.b.c` will not grant permissions
# to `a.b.c.d` if `explicit`=True
perms.check("a.b.c.d", "r", explicit=True)  # False
