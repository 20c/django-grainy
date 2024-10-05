from django.urls import include, re_path
from rest_framework import routers

from .views import (
    Detail,
    DetailExplicit,
    DetailManual,
    DetailReqFmt,
    ExplicitViewSet,
    JsonView,
    ModelAViewSet,
    View,
    detail,
    detail_explicit,
    view,
)

router = routers.DefaultRouter()
router.register(r"a", ModelAViewSet, basename="modela")
router.register(r"a_x", ExplicitViewSet, basename="explicit_modela")


urlpatterns = [
    re_path(r"^view/", view),
    re_path(r"^detail/(?P<id>[0-9]+)/$", detail),
    re_path(r"^detail_explicit/(?P<id>[0-9]+)/$", detail_explicit),
    re_path(r"^detail_class/(?P<id>[0-9]+)/$", Detail.as_view()),
    re_path(r"^detail_class_explicit/(?P<id>[0-9]+)/$", DetailExplicit.as_view()),
    re_path(r"^detail_class_reqfmt/(?P<id>[0-9]+)/$", DetailReqFmt.as_view()),
    re_path(r"^detail_class_manual/(?P<id>[0-9]+)/$", DetailManual.as_view()),
    re_path(r"^detail_class_manual/$", DetailManual.as_view()),
    re_path(r"^view_class/", View.as_view()),
    re_path(r"^view_class_json/", JsonView.as_view()),
    re_path(r"^", include(router.urls)),
    re_path(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
