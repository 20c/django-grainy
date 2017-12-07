import grainy.const

# literal namespace with integer permission flag
user.grainy_permissions.add_permission("a.b.c", grainy.const.READ)

# literal namespace with string permission flag
user.grainy_permissions.add_permission("a.b.c", "r")

# same for groups
group.grainy_permissions.add_permission("a.b.c", "r")
