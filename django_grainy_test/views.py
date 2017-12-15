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

@grainy_view(namespace="detail.{id}")
def detail(request, id):
    from django.urls import resolve
    print(resolve(request.path))
    return HttpResponse("ID {}".format(id))

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

@grainy_view(namespace="detail.{id}")
class Detail(BaseView):

    def get(self, request, id):
        return HttpResponse(content="GET Response {}".format(id))

    def post(self, request, id):
        return HttpResponse(content="POST Response {}".format(id))

    def put(self, request, id):
        return HttpResponse(content="PUT Response {}".format(id))

    def delete(self, request, id):
        return HttpResponse(content="DELETE Response {}".format(id))

    def patch(self, request, id):
        return HttpResponse(content="PATCH Response {}".format(id))


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
