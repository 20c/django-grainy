import six
from django.db import models

from .conf import PERM_CHOICES

class PermissionField(models.IntegerField):

    def to_python(self, value):
        # if a string is passed it should be parsed
        # for string flags (for example 'c', 'r', 'u' and 'd')
        # as specified in the PERM_CHOICES setting and
        # convert to bitmask
        if isinstance(value, six.string_types):
            _value = 0
            for flag, name, str_flag in PERM_CHOICES:
                if str_flag in value:
                    _value |= flag
            value = _value

        elif value is None:
            return 0

        return value


