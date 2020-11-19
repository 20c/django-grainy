from grainy.core import PermissionSet, Namespace

class GrainyHandler:
    """
    The base class to use for the Grainy Meta class
    """

    parent = None
    namespace_base = None
    namespace_instance_template = "{namespace}.{instance}"

    @classmethod
    def namespace_instance(cls, instance, **kwargs):
        """
        Returns the permissioning namespace for the passed instance

        Arguments:
            - instance <object|str|Namespace>: the value of this will be appended
                to the base namespace and returned

        Keyword Arguments:
            - any keyword arguments will be used for formatting of the
                namespace

        Returns:
            - unicode: namespace
        """

        if not isinstance(cls.namespace_base, Namespace):
            raise ValueError("`namespace_base` needs to be a Namespace instance")
        template = cls.namespace_instance_template

        if instance == "*":
            if "id" not in kwargs:
                kwargs.update(id="*")
            template = template.replace("{instance.","{")
        if kwargs.get("pk") is None:
            kwargs.update(pk=kwargs.get("id"))


        return template.format(
            namespace=str(cls.namespace_base).format(**kwargs),
            instance=instance,
            **kwargs,
        ).lower()

    @classmethod
    def namespace(cls, instance=None, **kwargs):
        """
        Wrapper function to return either the result of namespace_base or
        namespace instance depending on whether or not a value was passed in
        `instance`

        All keyword arguments will be available while formatting the
        namespace string.

        Keyword Arguments:
            - instance <object|str|Namespace>: the value of this will be appended

        Returns:
            - unicode
        """
        if instance:
            return cls.namespace_instance(instance, **kwargs)
        namespace = f"{cls.namespace_base}"
        if kwargs:
            namespace = namespace.format(**kwargs)
        return namespace.lower()

    @classmethod
    def set_namespace_base(cls, value):
        if not isinstance(value, Namespace):
            raise TypeError("`value` needs to be a Namespace instance")
        cls.namespace_base = value

    @classmethod
    def set_parent(cls, parent):
        cls.parent = parent


class GrainyModelHandler(GrainyHandler):

    """
    grainy model handler meta class
    """

    model = None
    namespace_instance_template = "{namespace}.{instance.pk}"

    @classmethod
    def set_parent(cls, model):
        cls.parent = model
        cls.model = model
        cls.set_namespace_base(
            Namespace([model._meta.app_label, model._meta.object_name])
        )


class GrainyMixin:
    @property
    def grainy_namespace(self):
        return self.Grainy.namespace(self)
