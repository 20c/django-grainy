class DecoratorRequiresNamespace(ValueError):
    def __init__(self, decorator):
        super(DecoratorRequiresNamespace, self).__init__(
            "This decorator requires you to specify a namespace"
        )
        self.decorator = decorator
