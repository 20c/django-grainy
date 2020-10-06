import six
import inspect
from grainy.core import (
    Namespace,
)
from .conf import PERM_CHOICES, REQUEST_METHOD_TO_FLAG, DJANGO_OP_TO_FLAG


def namespace(target, **kwargs):

    """
    Convert `target` to permissioning namespace

    Any keyword arguments will be used for formatting of the
    namespace (as applicable)

    Arguments:
        - target <object|class|string|tuple>: if an object or class is passed here it
            will be required to contain a `Grainy` meta class, otherwise a
            TypeError will be raised.

            If a tuple is passed all elements of the tuple will be passed to
            the namespace function individually and the resulting namespaces will
            be joined together and returned as one namespace string

    Returns:
        - string
    """

    if not target:
        return ""

    if isinstance(target, tuple) or isinstance(target, list):
        result = []
        for _t in target:
            result.append(namespace(_t))
        return str(Namespace(result))

    handler_class = getattr(target, "Grainy", None)

    if inspect.isclass(handler_class):
        if inspect.isclass(target):
            return target.Grainy.namespace(**kwargs)
        return target.Grainy.namespace(instance=target, **kwargs)

    if isinstance(target, str):
        return target

    raise TypeError(
        f"`target` {target} could not be convered to a permissioning namespace"
    )


def dict_get_namespace(data, namespace):
    d = data
    path = []
    for k in namespace:
        if k not in d:
            raise KeyError("`{}` does not exist at `{}`".format(k, ".".join(path)))
        path.append(k)
        d = d[k]
    return d


def request_to_flag(request):
    """
    Returns the appropriate grainy permission flag for the request
    depending on the request's method.

    Arguments:
        - request <Request>: django request object

    Returns:
        - int
    """
    return request_method_to_flag(request.method)


def request_method_to_flag(method):
    """
    Converts a request method to the matching grainy permission
    flag

    Arguments:
        - method <str>: request method 'GET', 'POST' etc.

    Returns:
        - int
    """
    return REQUEST_METHOD_TO_FLAG.get(method.upper(), 0)


def django_op_to_flag(op):
    """
    Converts a django admin operation string to the matching
    grainy permission flag

    Arguments:
        - op <str>

    Returns:
        - int
    """
    return DJANGO_OP_TO_FLAG.get(op, 0)


def int_flags(flags):
    """
    Converts string permission flags into integer permission flags

    Arguments:
        - flags <str>: one or more flags as they are defined in GRAINY_PERM_CHOICES

            For example: "crud" or "ru" or "r"

    Returns:
        - int
    """

    r = 0
    if not flags:
        return r

    if isinstance(flags, int):
        return flags

    if not isinstance(flags, str):
        raise TypeError("`flags` needs to be a string or integer type")

    for f in flags:
        for f_i, name, f_s in PERM_CHOICES:
            if f_s == f:
                r = r | f_i
    return r


def str_flags(flags):
    """
    Converts integer permission flags into string permission flags

    Arguments:
        - flags <int>: one or more flags as they are defined in GRAINY_PERM_CHOICES

            For example: PERM_READ or PERM_READ | PERM_UPDATE

    Returns:
        - str
    """

    r = ""
    if not flags:
        return r

    if isinstance(flags, str):
        return flags

    if not isinstance(flags, int):
        raise TypeError("`flags` needs to be a string or integer type")

    for f_i, name, f_s in PERM_CHOICES:
        if flags & f_i:
            r += f_s
    return r
