import six
from django.db import models
from django import forms
from .conf import PERM_CHOICES


class PermissionFormField(forms.IntegerField):
    def prepare_value(self, value):
        # if the form field is passed a bitmask we
        # need to convert it to a list, where each
        # item represents a choice (flag)
        if isinstance(value, int):
            _value = []
            for f, n, c in PERM_CHOICES:
                if value & f:
                    _value.append(f)
            value = _value
        else:
            value = value or 0
        return value

    def clean(self, value):
        if isinstance(value, list):
            _value = 0
            for flag in value:
                _value |= int(flag)
            value = _value
        return value


class PermissionField(models.IntegerField):
    def to_python(self, value):
        # if a string is passed it should be parsed
        # for string flags (for example 'c', 'r', 'u' and 'd')
        # as specified in the PERM_CHOICES setting and
        # convert to bitmask
        if isinstance(value, str):
            _value = 0
            for flag, name, str_flag in PERM_CHOICES:
                if str_flag in value:
                    _value |= flag
            value = _value
        elif value is None:
            return 0

        return value
