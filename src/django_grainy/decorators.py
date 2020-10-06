import inspect
import json

from types import MethodType

from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder

from django.views import View
from django.http import HttpRequest

from grainy.core import Namespace

from .models import GrainyHandler, GrainyModelHandler
from .util import Permissions
from .exceptions import (
    DecoratorRequiresNamespace,
)
from .helpers import namespace, dict_get_namespace, request_to_flag


class grainy_decorator:

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

    def __init__(self, namespace=None, namespace_instance=None, **kwargs):
        self.namespace = namespace
        self.namespace_instance = namespace_instance
        self.extra = kwargs
        self.permissions_cls = kwargs.get("permissions_cls", Permissions)
        if self.require_namespace and not namespace:
            raise DecoratorRequiresNamespace(self)

    def make_grainy_handler(self, target):
        class Grainy(self.handler_class):
            pass

        Grainy.set_parent(target)

        if not target and not self.namespace:
            raise DecoratorRequiresNamespace(self)

        if self.namespace is not None:
            Grainy.set_namespace_base(Namespace(namespace(self.namespace)))

        if self.namespace_instance is not None:
            Grainy.namespace_instance_template = namespace(self.namespace_instance)

        return Grainy


class grainy_model(grainy_decorator):

    """
    Initialize grainy permissions for the targeted model

    Keyword Arguments:
        - parent <str>: name of a ForeignKey field on the model, if specified
            the instance namespace will be built, prefixing the instance namespace
            from the parent model.

            Use this to quickly do namespace inheritance.
    """

    handler_class = GrainyModelHandler

    def __init__(self, namespace=None, parent=None, **kwargs):
        self.parent = parent
        return super().__init__(namespace=namespace, **kwargs)

    def __call__(self, model):
        model.Grainy = self.make_grainy_handler(model)
        if self.parent:
            model.Grainy.parent_field = self.parent
            model.Grainy.parent_model = model._meta.get_field(
                self.parent
            ).remote_field.model
            self.parent_namespacing(model)

        return model

    def parent_namespacing(self, model):
        namespace = [model.Grainy.namespace(), "{instance.pk}"]
        fields = ["instance"]

        parent = model.Grainy.parent_model
        parent_field = model.Grainy.parent_field

        while parent:
            fields += [parent_field]
            namespace = [
                parent.Grainy.namespace(),
                "{" + ".".join(fields) + ".pk}",
            ] + namespace
            _parent = getattr(parent.Grainy, "parent_model", None)
            if _parent:
                parent_field = parent.Grainy.parent_field
            parent = _parent

        # namespace = [parent.Grainy.namespace] + namespace
        model.Grainy.namespace_instance_template = ".".join(namespace)


class grainy_view_response(grainy_decorator):

    """
    Initialize grainy permissions for the targeted view

    Keyword Arguments:
        - explicit <bool> - if true, permissions checks during
            request gating will be explicit (default=False)
        - explicit_instance <bool|None> - if true, permission checks during
            requests to response handlers that provide an object instance
            via view.get_object() will require explicit permissions.
            if None, value will be inherited from `explicit` keyword argument.
            (default=None)
        - ignore_grant_all <bool> - if true, permissions checks during
            request gating will ignore superuser priviledges (default=False)
    """

    # There is no way to make a sensible namespace from
    # a view class or function, so a manual namespace always
    # needs to be set in decorator
    require_namespace = True

    view = None

    def __call__(self, view_function):

        get_object = self.get_object
        apply_perms = self.apply_perms
        extra = self.extra
        permissions_cls = self.permissions_cls
        decorator = self

        grainy_handler = self.make_grainy_handler(view_function)

        def response_handler(*args, **kwargs):
            if isinstance(args[0], HttpRequest):
                self = None
                request = args[0]
            else:
                self = args[0]
                request = args[1]

            perms = permissions_cls(request.user)
            obj = get_object(self)

            # prepare parameters for namespace formatting
            nsparam = {"request": request}
            nsparam.update(kwargs)
            nsparam.update(request.GET)

            # check base namespace permissions
            if not perms.check(
                grainy_handler.namespace(**nsparam).format(**nsparam),
                request_to_flag(request),
                explicit=extra.get("explicit", False),
                ignore_grant_all=extra.get("ignore_grant_all", False),
            ):
                return HttpResponse(status=403)

            nsparam["instance"] = obj

            # if object was retrieved, check object permissions as well
            if obj and not perms.check(
                grainy_handler.namespace(**nsparam).format(**nsparam),
                request_to_flag(request),
                explicit=extra.get("explicit_instance", extra.get("explicit", False)),
                ignore_grant_all=extra.get("ignore_grant_all", False),
            ):
                return HttpResponse(status=403)

            request.nsparam = nsparam

            decorator.augment_request(request)

            return apply_perms(
                request, view_function(*args, **kwargs), view_function, self
            )

        grainy_handler.view = self.extra.get("view")
        response_handler.Grainy = self.Grainy = grainy_handler
        response_handler.__name__ = view_function.__name__
        return response_handler

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

    def apply_perms(self, request, response, view_function, view):
        """
        Apply permissions to the generated response
        """
        return response

    def augment_request(self, request):
        """
        Augment the request instance
        """
        return request


class grainy_json_view_response(grainy_view_response):

    """
    A view response handler that will apply grainy permissions to
    the json data in the generated response, removing any content the
    requesting user does not have `READ` permissions to

    Keyword Arguments:
        - decoder: allows you to specify a json decoder class
        - encoder: allows you to specify a json encoder class
        - safe <bool>: passed to DjangoJSONEncoder
        - json_dumps_params <dict>: passed to DjangoJSONEncoder
    """

    def _apply_perms(self, request, data, view_function, view):
        perms = self.permissions_cls(request.user)
        try:
            obj = self.get_object(view)
        except AssertionError as inst:
            obj = None
        namespace = Namespace(
            self.Grainy.namespace(**request.nsparam).replace("?", "*")
        )

        if isinstance(data, list):
            prefix = f"{namespace}.*"
        else:
            prefix = namespace
        for ns, p in self.extra.get("handlers", {}).items():
            perms.applicator.handler(f"{prefix}.{ns}", **p)

        data, tail = namespace.container(data)

        data = perms.apply(data)
        try:
            return dict_get_namespace(data, namespace)
        except KeyError as inst:
            pass
        if isinstance(tail, list):
            return []
        else:
            return {}

    def apply_perms(self, request, response, view_function, view):
        response.content = JsonResponse(
            self._apply_perms(
                request,
                json.loads(
                    response.content.decode("utf-8"), cls=self.extra.get("decoder")
                ),
                view_function,
                view,
            ),
            encoder=self.extra.get("encoder", DjangoJSONEncoder),
            safe=self.extra.get("safe", True),
            json_dumps_params=self.extra.get("json_dumps_params"),
        )
        return response


class grainy_rest_viewset_response(grainy_json_view_response):

    """
    Initialize grainy permissions for the targeted rest
    framework viewset response.

    This will apply the permissions to the data returned
    in the viewset response. Any fields that the requesting
    user does not have READ permissions to will get dropped
    from the data

    It will also gate the various request handlers behind the
    appropriate permissions.
    """

    require_namespace = True

    def get_object(self, view):
        try:
            return super().get_object(view)
        except AssertionError as inst:
            return None

    def apply_perms(self, request, response, view_function, view):
        response.data = self._apply_perms(request, response.data, view_function, view)
        return response

    def augment_request(self, request):
        """
        Augments the request by adding the following methods

        - `grainy_data(defaults)`: returns a copy of request.data with grainy
        permissions applied.
        - `grainy_update_serializer(serializer_cls, instance, **kwargs)`: returns
        a drf serializer instance for create / update. Data will be cleaned against
        grainy permissions
        """

        decorator = self
        namespace = Namespace(
            self.Grainy.namespace(**request.nsparam).replace("?", "*")
        )
        perms = decorator.permissions_cls(request.user)

        def grainy_data(request, defaults):

            """
            Returns a cleaned up dict for request.data

            Any fields that are permissioned to be writeable by
            the request will have their values applied to the
            result.

            Any fields that are NOT permissioned to be writeable
            by the request will fall back to their values in
            `defaults`
            """

            if request.method in ["PUT", "PATCH"]:
                op = "u"
            elif request.method == "POST":
                op = "c"
            else:
                return request.data

            data = defaults

            for field, value in request.data.items():
                if perms.check([f"{namespace}", field], op):
                    data[field] = value

            return data

        def grainy_update_serializer(serializer_cls, instance, **kwargs):
            """
            returns a django-rest-framework serializer instance with
            for saves.

            Will automatically apply grainy_data to the input data.
            """
            if instance:
                data = grainy_data(request, serializer_cls(instance=instance).data)
            else:
                data = grainy_data(request, {})
            return serializer_cls(data=data, instance=instance, **kwargs)

        request.grainy_data = lambda defaults: grainy_data(request, defaults)
        request.grainy_update_serializer = grainy_update_serializer

        return request


class grainy_view(grainy_decorator):

    """
    Applies `grainy_view_response` decorators to all response
    handlers in the decorated view.

    Response handlers that already have been made grainy manually
    or otherwise will be skipped
    """

    # the response handlers that will be affected by grainy
    # permissions
    response_handlers = ["get", "post", "put", "delete", "patch", "head", "options"]

    decorator = grainy_view_response
    require_namespace = True

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args, **kwargs)

    def __call__(self, view):

        view.Grainy = self.make_grainy_handler(view)

        if inspect.isclass(view):
            self.kwargs["view"] = view
            for rh in self.response_handlers:
                if hasattr(view, rh):
                    view_function = getattr(view, rh)
                    if (
                        not hasattr(view_function, "Grainy")
                        or view_function.Grainy.view
                    ):
                        setattr(view, rh, self.decorate(view_function))
                    else:
                        print(view_function, view_function.Grainy)
            return view
        else:
            return self.decorate(view)

    def decorate(self, view):
        return self.decorator(*self.args, **self.kwargs)(view)


class grainy_json_view(grainy_view):

    """
    Applies `grainy_json_view_response` decorators to all response
    handlers in the decorated view.

    Response handlers that already have been made grainy manually
    or otherwise will be skipped
    """

    decorator = grainy_json_view_response


class grainy_rest_viewset(grainy_json_view):

    """
    Applies `grainy_rest_viewset_response` decorators to all response
    handlers in the decorated view.

    Response handlers that already have been made grainy manually
    or otherwise will be skipped
    """

    response_handlers = [
        "list",
        "retrieve",
        "create",
        "update",
        "partial_update",
        "destroy",
    ]

    decorator = grainy_rest_viewset_response
