class DecoratorRequiresNamespace(ValueError):
    def __init__(self, decorator):
        super().__init__("This decorator requires you to specify a namespace")
        self.decorator = decorator

class PermissionDenied(Exception):
    def __init__(self, reason):
        super(PermissionDenied, self).__init__(f"Permission denied: {reason}")
