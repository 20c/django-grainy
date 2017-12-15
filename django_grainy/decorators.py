import inspect
import json

from types import MethodType

from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder

from grainy.core import Namespace

from .models import (
    GrainyHandler,
    GrainyModelHandler
)
from .util import Permissions
from .exceptions import (
    DecoratorRequiresNamespace,
)
from .helpers import (
    dict_get_namespace,
    request_to_flag
)


class grainy_decorator(object):

    """
    base decorator that all the other grainy_* decorators
    extend from

    Keyword Arguments:
        - namespace <str>: the permissioning namespace for this decorator
        - handlers <dict>: grainy applicator handlers
    """

    handler_class = GrainyHandler

    # if true, this decorator cannot have a None namespace
    require_namespace = False

    def __init__(self, namespace=None, **kwargs):
        self.namespace = namespace
        self.extra = kwargs
        if self.require_namespace and not namespace:
            raise DecoratorRequiresNamespace(self)

    def make_grainy_handler(self, target):
        class Grainy(self.handler_class):
            pass
        Grainy.set_parent(target)

        if not target and not self.namespace:
            raise DecoratorRequiresNamespace(self)

        if self.namespace is not None:
            namespace = Namespace(self.namespace)
            Grainy.set_namespace_base(namespace)
        return Grainy


class grainy_model(grainy_decorator):

    """
    Initialize grainy permissions for the targeted model
    """

    handler_class = GrainyModelHandler

    def __call__(self, model):
        model.Grainy = self.make_grainy_handler(model)
        return model


class grainy_view(grainy_decorator):

    """
    Initialize grainy permissions for the targeted view
    """

    # There is no way to make a sensible namespace from
    # a view class or function, so a manual namespace always
    # needs to be set in decorator
    require_namespace = True

    # the response handlers that will be affected by grainy
    # permissions
    response_handlers = [
        "get",
        "post",
        "put",
        "delete",
        "patch",
        "head",
        "options"
    ]

    def __call__(self, view):
        get_object = self.get_object
        apply_perms = self.apply_perms

        if inspect.isclass(view):

            # handle class views

            class GrainyView(view):

                def sanitize(self, request, response):

                    """
                    Sanitizes the response returned by the request according
                    to grainy permissions
                    """

                    return apply_perms(
                        request,
                        response,
                        self
                    )

                def gate(self, request, *args, **kwargs):

                    """
                    Gates the request behind grainy permissions depending
                    on the request.method
                    """

                    perms = Permissions(request.user)

                    if not perms.check(
                        self.Grainy.namespace(get_object(self)).format(**kwargs),
                        request_to_flag(request)
                    ):
                        return HttpResponse(status=403)
                    return None

            GrainyView.__name__ = view.__name__
            GrainyView.Grainy = self.make_grainy_handler(view)

            # dynamically add response handler methods to the grainy view
            # class

            for n in self.response_handlers:
                def _response(_self, request, handler_name=n, *args, **kwargs):
                    gated_response = _self.gate(request, *args, **kwargs)
                    if gated_response:
                        return gated_response
                    fn = getattr(super(GrainyView, _self), handler_name.lower(), None)
                    if not fn:
                        return HttpResponse()
                    return _self.sanitize(request, fn(request, *args, **kwargs))
                setattr(GrainyView, n, _response)

            return GrainyView

        else:

            # handle function view

            view.Grainy = self.make_grainy_handler(view)
            def grainy_view(request, *args, **kwargs):
                perms = Permissions(request.user)
                if not perms.check(
                    view.Grainy.namespace(get_object(view)).format(**kwargs),
                    request_to_flag(request)
                ):
                    return HttpResponse(status=403)
                return apply_perms(request, view(request, *args, **kwargs), self)

            grainy_view.Grainy = view.Grainy
            return grainy_view

    def get_object(self, view):
        """
        Attempts to call and return `get_object` on the decorated view. 

        If implemented on the decorated view it should return an object instance
        relevant to the request that can be used to pass to the namespace getter
        of the GrainyHandler - in most cases this would be a model instance
        """
        if hasattr(view, "get_object"):
            return view.get_object()
        return None

    def apply_perms(self, request, response, view):
        """
        Apply permissions to the generated response
        """
        return response



class grainy_json_view(grainy_view):

    """
    A view that will apply grainy permissions to the json data
    in the generated response, removing any content the requesting
    user does not have `READ` permissions to

    Keyword Arguments:
        - decoder: allows you to specify a json decoder class
        - encoder: allows you to specify a json encoder class
        - safe <bool>: passed to DjangoJSONEncoder
        - json_dumps_params <dict>: passed to DjangoJSONEncoder
    """

    def _apply_perms(self, request, data, view):
        perms = Permissions(request.user)
        try:
            obj = self.get_object(view)
        except AssertionError as inst:
            obj = None
        namespace = Namespace(view.Grainy.namespace(obj))

        if isinstance(data, list):
            prefix = "{}.*".format(namespace)
        else:
            prefix = namespace
        for ns,p in self.extra.get("handlers", {}).items():
            perms.applicator.handler("{}.{}".format(prefix, ns), **p)

        data, tail = namespace.container(data)
        data = perms.apply(data)
        try:
            return dict_get_namespace(data, namespace)
        except KeyError as inst:
            return {}

    def apply_perms(self, request, response, view):
        response.content = JsonResponse(
            self._apply_perms(
                request, json.loads(
                    response.content.decode("utf-8"),
                    cls = self.extra.get("decoder")
                ), view
            ),
            encoder = self.extra.get("encoder", DjangoJSONEncoder),
            safe = self.extra.get("safe", True),
            json_dumps_params = self.extra.get("json_dumps_params")
        )
        return response


class grainy_rest_viewset(grainy_json_view):

    """
    Initialize grainy permissions for the targeted rest 
    framework viewset.

    This will apply the permissions to the data returned 
    in the viewset response. Any fields that the requesting
    user does not have READ permissions to will get dropped
    from the data

    It will also gate the various request handlers behind the
    appropriate permissions.
    """

    require_namespace = True
    response_handlers = [
        "list",
        "retrieve",
        "create",
        "update",
        "partial_update",
        "destroy"
    ]

    def get_object(self, view):
        try:
            return super(grainy_rest_viewset, self).get_object(view)
        except AssertionError as inst:
            return None

    def apply_perms(self, request, response, view):
        response.data = self._apply_perms(request, response.data, view)
        return response
