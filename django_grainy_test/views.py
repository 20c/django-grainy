# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View as BaseView

from rest_framework import viewsets
from django_grainy.decorators import (
    grainy_view,
    grainy_json_view,
    grainy_rest_viewset,
)

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

@grainy_view(namespace="site.view")
def view(request):
    return HttpResponse()

@grainy_view(namespace="site.view")
class View(BaseView):
    def get(self, request):
        return HttpResponse(content="GET Response")

    def post(self, request):
        return HttpResponse(content="POST Response")

    def put(self, request):
        return HttpResponse(content="PUT Response")

    def delete(self, request):
        return HttpResponse(content="DELETE Response")

    def patch(self, request):
        return HttpResponse(content="PATCH Response")

@grainy_json_view(
    namespace="site.view",
    handlers = {
        "nested_dict.secret" : { "explicit" : True }
    }
)
class JsonView(BaseView):
    def get(self, request):
        return JsonResponse({
            "hello" : "world",
            "nested_dict" : {
                "public": "something",
                "secret": "hidden"
            }
        })
