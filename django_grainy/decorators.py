from grainy.core import Namespace
from .models import GrainyHandler as _GrainyHandler
from .util import Permissions
from .exceptions import (
    DecoratorRequiresNamespace,
)
from .helpers import (
    dict_get_namespace,
)


class grainy_decorator(object):

    """
    base decorator that all the other grainy_* decorators
    extend from

    Keyword Arguments:
        - namespace <str>: the permissioning namespace for this decorator
        - handlers <dict>: grainy applicator handlers
    """

    # if true, this decorator cannot have a None namespace
    require_namespace = False

    def __init__(self, namespace=None, **kwargs):
        self.namespace = namespace
        self.extra = kwargs
        if self.require_namespace and not namespace:
            raise DecoratorRequiresNamespace(self)

    def make_grainy_handler(self, model):
        class Grainy(_GrainyHandler):
            pass
        Grainy.model = model

        if not model and not self.namespace:
            raise DecoratorRequiresNamespace(self)

        if self.namespace is not None:
            namespace = self.namespace

            @classmethod
            def namespace_model(cls):
                return namespace.lower()
            Grainy.namespace_model = namespace_model
        return Grainy



class grainy_model(grainy_decorator):

    """
    Initialize grainy permissions for the targeted model
    """

    def __call__(self, model):
        model.Grainy = self.make_grainy_handler(model)
        return model


class grainy_view(grainy_decorator):

    """
    Initialize grainy permissions for the targeted view
    """

    require_namespace = True

    def __call__(self, view):
        view.Grainy = self.make_grainy_handler(view)


class grainy_rest_view(grainy_view):
    pass


class grainy_rest_viewset(grainy_decorator):

    """
    Initialize grainy permissions for the targeted rest 
    framework viewset.

    This will apply the permissions to the data returned 
    in the viewset response. Any fields that the requesting
    user does not have READ permissions to will get dropped
    from the data
    """

    require_namespace = True

    def __call__(self, viewset):
        viewset.Grainy = self.make_grainy_handler(viewset)

        extra = self.extra

        class GrainyViewset(viewset):

            def retrieve(self, request, pk):
                response = super(GrainyViewset, self).retrieve(request, pk)
                return self.apply_perms(request, response)

            def list(self, request):
                response = super(GrainyViewset, self).list(request)
                return self.apply_perms(request, response)

            def apply_perms(self, request, response):
                perms = Permissions(request.user)
                namespace = Namespace(self.Grainy.namespace())

                if isinstance(response.data, list):
                    prefix = "{}.*".format(namespace)
                else:
                    prefix = namespace
                for ns,p in extra.get("handlers", {}).items():
                    perms.applicator.handler("{}.{}".format(prefix, ns), **p)

                data, tail = namespace.container(response.data)
                data = perms.apply(data)
                try:
                    response.data = dict_get_namespace(data, namespace)
                except KeyError as inst:
                    response.data = {}

                return response
        GrainyViewset.__name__ = viewset.__name__
        return GrainyViewset
