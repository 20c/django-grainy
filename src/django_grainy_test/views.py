from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View as BaseView

from rest_framework import viewsets
from django_grainy.decorators import (
    grainy_view,
    grainy_json_view,
    grainy_rest_viewset,
    grainy_rest_viewset_response,
    grainy_view_response,
)

from .models import ModelA
from .serializers import ModelASerializer

# Create your views here.


@grainy_rest_viewset(
    namespace="api.a", handlers={"nested_dict.secret": {"explicit": True}}
)
class ModelAViewSet(viewsets.ModelViewSet):
    queryset = ModelA.objects.all()
    serializer_class = ModelASerializer


class ExplicitViewSet(viewsets.ModelViewSet):
    queryset = ModelA.objects.all()
    serializer_class = ModelASerializer

    @grainy_rest_viewset_response(
        namespace="api.a_x",
        namespace_instance="{namespace}.{instance.id}",
        explicit=True,
        explicit_instance=False,
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @grainy_rest_viewset_response(
        namespace="api.a_x",
        namespace_instance="{namespace}.{instance.id}",
        explicit=True,
    )
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)


@grainy_view(namespace="site.view")
def view(request):
    return HttpResponse()


@grainy_view(namespace="detail.{id}")
def detail(request, id):
    return HttpResponse(f"ID {id}")


@grainy_view(namespace="detail.{id}", explicit=True, ignore_grant_all=True)
def detail_explicit(request, id):
    return HttpResponse(f"ID {id}")


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
        return HttpResponse(content=f"GET Response {id}")

    def post(self, request, id):
        return HttpResponse(content=f"POST Response {id}")

    def put(self, request, id):
        return HttpResponse(content=f"PUT Response {id}")

    def delete(self, request, id):
        return HttpResponse(content=f"DELETE Response {id}")

    def patch(self, request, id):
        return HttpResponse(content=f"PATCH Response {id}")


@grainy_view(namespace="detail.{id}", explicit=True, ignore_grant_all=True)
class DetailExplicit(Detail):
    pass


@grainy_view(namespace="detail_manual.{id}")
class DetailManual(BaseView):
    def get(self, request, id):
        return HttpResponse(content=f"GET Response {id}")

    @grainy_view_response(namespace="detail_manual")
    def post(self, request):
        return HttpResponse(content="POST Response 1")


@grainy_view(namespace="detail_manual.{request.method}.{id}")
class DetailReqFmt(Detail):
    pass


@grainy_json_view(
    namespace="site.view", handlers={"nested_dict.secret": {"explicit": True}}
)
class JsonView(BaseView):
    def get(self, request):
        return JsonResponse(
            {
                "hello": "world",
                "nested_dict": {"public": "something", "secret": "hidden"},
            }
        )
