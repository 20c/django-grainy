"""
Implements a solution for remote grainy permission loading

Providing django instance needs to expose ProvideGet and/or ProvideLoad
views.

Requesting django instance can than use the remote.Permissions utility
to request and check permissions from the provider.
"""
import json

from grainy.core import PermissionSet
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.core.cache import cache

from grainy.core import Permission

import django_grainy.util

from .conf import ANONYMOUS_PERMS


# Soft requirement import of requests module
# Error will be raised if remote Permissions
# are instantiated and it is missing

try:
    import requests
except ImportError:
    requests = None


class JSONEncoder(json.JSONEncoder):

    """
    JSONEncoder that can handle grainy permission
    value serialization
    """

    def default(self, obj):
        if isinstance(obj, Permission):
            return obj.value
        return super().default(obj)


class Authenticator:
    """
    Implements authentication logic to use when
    requesting grainy permissions from the provider

    Defaults to simply passing the request through as
    is.
    """

    def authenticate(self, request):
        pass


class Provider(View):

    """
    Base provider class

    Extended django view that implements an authentication
    override for the incoming request to allow grainy
    to properly identify the user for which it is to return
    permission information
    """

    @classmethod
    def as_view(cls, authenticator_cls=Authenticator, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        cls.authenticator_cls = authenticator_cls
        return view

    def authenticate(self, request):
        self.authenticator_cls().authenticate(request)
        self.permissions = django_grainy.util.Permissions(request.user)


class ProvideGet(Provider):

    """
    Provide integer permission flag for the passed
    namespace
    """

    def get(self, request, namespace):
        self.authenticate(request)
        as_string = bool(request.GET.get("as_string", 0))
        explicit = bool(request.GET.get("explicit", 0))
        return HttpResponse(self.permissions.get(namespace))


class ProvideLoad(Provider):

    """
    Provide full permission set (dict)
    """

    def get(self, request):
        self.authenticate(request)
        return JsonResponse(
            self.permissions.pset.permissions,
            json_dumps_params={"indent": 2},
            encoder=JSONEncoder,
        )


class Permissions(django_grainy.util.Permissions):

    """
    Remote permissions util

    Requests permission values from a remote
    grainy provider


    """

    def __init__(self, obj, url_load=None, url_get=None, cache=5):
        """
        Arguments:
        - obj (`User`|`AnonymousUser`|`Group`|Model`)


        Keyword Arguments:
        - url_load (`str`): url to grainy load provider
        - url_get (`str`): url to grainy get provider
        - cache (`int`): cache requests for n seconds
        """

        if not url_load and not url_get:
            raise ValueError("At a minium either url_load or url_get need to specified")

        self.url_load = url_load
        self.url_get = url_get
        self.obj = obj
        self.pset = PermissionSet()
        self.applicator = django_grainy.util.Applicator(self.pset)
        self.loaded = False
        self.grant_all = (
            isinstance(obj, django_grainy.util.get_user_model()) and obj.is_superuser
        )
        self.cache = cache

    def fetch(self, url, cache_key, **params):

        """
        Retrieve grainy permissions from remote endpoint

        Arguments:
        - url (`str`)
        - cache_key (`str`)

        Keyword Arguments:
        - any keyword args provided will be passed along in the
        the request's url parameters
        """

        if self.cache > 0:
            cached = cache.get(cache_key)
            if cached:
                return json.loads(cached)

        headers = {}
        self.prepare_request(params, headers)
        data = requests.get(url, params=params, headers=headers)

        data = data.json()

        if self.cache > 0:
            cache.set(cache_key, json.dumps(data), self.cache)

        return data

    def load(self, refresh=False):
        """
        Load permission set from the remote provider

        This requires `url_load` property to be specified

        Keyword Arguments:

        - refresh (`bool`): if True will force a refresh
        """
        if not self.url_load or isinstance(self.obj, django_grainy.util.AnonymousUser):
            self.pset = PermissionSet()
            return

        if not self.loaded or refresh:
            self.pset = PermissionSet()
            cache_key = f"grainy:load:{self.obj.id}"
            self.pset.update(self.fetch(self.url_load, cache_key))
            self.loaded = True

    def get(self, target, as_string=False, explicit=False):
        """
        Retrieve permission flags for the specified target namespace
        from the remote provider

        If `url_load` is specified this will first call load() and
        then use the provided permission set to return the result

        Otherwise `url_get` will be requested for a direct remote
        result for the target namespace

        Arguments:
        - target (`object|class|str`): return permissions to this object /
          namespsace

        Keyword Arguments:
        - as_string (`bool`): if True returns string flags instead of int flags
        - explicit (`bool`): require explicit permissions to the complete target

        Returns:
        - (`int`): permission flags
        - (`str`): permission flags, if as_string=True
        """
        if self.url_load:
            self.load()
            return super().get(*args, **kwargs)
        else:
            target = django_grainy.util.namespace(target)
            cache_key = f"grainy:get:{self.obj.id}:{target}"
            r = self.fetch(
                self.url_get.format(namespace=target),
                cache_key,
                as_string=as_string,
                explicit=explicit,
            )
            if as_string:
                return django_grainy.util.str_flags(r)
            return int(r)

    def check(self, target, permissions, explicit=False, **kwargs):
        if self.url_load:
            self.load()
            return super().check(
                target, permissions, explicit=explicit, ignore_grant_all=True
            )
        else:
            perms = self.get(target, explicit=explicit)
            return perms & django_grainy.util.int_flags(permissions) != 0

    def apply(self, *args, **kwargs):
        if not self.url_load:
            raise NotImplementedError(
                "Specify `url_load` in order to use `apply` with remote permissions"
            )
        self.load()
        return super().apply(*args, **kwargs)

    def instances(self, *args, **kwargs):
        if not self.url_load:
            raise NotImplementedError(
                "Specify `url_load` in order to use `instances` with remote permissions"
            )

        self.load()
        return super().instances(*args, **kwargs)

    def prepare_request(self, params, headers):
        """
        When extending can override this to augment the request
        with extra url parameters and headers before it is sent
        to the remote providers
        """
        pass
