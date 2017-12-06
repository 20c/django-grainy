# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from django_grainy.decorators import grainy_rest_viewset

from .models import ModelA
from .serializers import ModelASerializer

# Create your views here.

@grainy_rest_viewset(
    namespace = "api.a",
    handlers = {
        "nested_dict.secret" : { "explicit" : True }
    }
)
class ModelAViewSet(viewsets.ModelViewSet):
    queryset = ModelA.objects.all()
    serializer_class = ModelASerializer
