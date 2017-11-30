import six
from .conf import PERM_CHOICES

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

    if isinstance(flags, six.integer_types):
        return flags

    if not isinstance(flags, six.string_types):
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

    if isinstance(flags, six.string_types):
        return flags

    if not isinstance(flags, six.integer_types):
        raise TypeError("`flags` needs to be a string or integer type")

    for f_i, name, f_s in PERM_CHOICES:
        if flags & f_i:
            r += f_s
    return r




