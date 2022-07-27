from typing import Any, Callable


class DecoratorRequiresNamespace(ValueError):
    def __init__(self, decorator: Callable):
        super().__init__("This decorator requires you to specify a namespace")
        self.decorator = decorator


class PermissionDenied(Exception):
    def __init__(self, reason: Any):
        super().__init__(f"Permission denied: {reason}")
