from django_grainy.util import Permissions

# give user full permissions to model (any instance)
user.grainy_permissions.add(TestModelA, "crud")

# give user full permissions to a specific instance
instance = TestModelA.objects.get(id=1)
user.grainy_permissions.add(instance, "crud")

# check user permission on model class
perms = Permissions(user)
perms.check(TestModelA, "r") # True

# check user permission on instance
perms.check(instance, "r") # True

# check permissions to the name field
perms.check( (instance, "name"), "r")

# return all instances of the model according to permissions
instances = perms.instances(TestModelA, "r")
