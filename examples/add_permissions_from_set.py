import grainy.const
import grainy.core

# set from PermissionSet instance
user.grainy_permissions.add_permission_set(
    grainy.core.PermissionSet({
        "a.b.c" : grainy.const.PERM_READ
    })
)

# set from dict (allows string permissions)
user.grainy_permissions.add_permission_set(
    {
        "a.b.c" : "r"
    }
)
