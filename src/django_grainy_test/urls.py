from django.conf.urls import url, include
from rest_framework import routers
from .views import (
    ModelAViewSet,
    ExplicitViewSet,
    JsonView,
    View,
    view,
    Detail,
    detail,
    DetailExplicit,
    detail_explicit,
    DetailManual,
    DetailReqFmt,
)

router = routers.DefaultRouter()
router.register(r"a", ModelAViewSet)
router.register(r"a_x", ExplicitViewSet)


urlpatterns = [
    url(r"^view/", view),
    url(r"^detail/(?P<id>[0-9]+)/$", detail),
    url(r"^detail_explicit/(?P<id>[0-9]+)/$", detail_explicit),
    url(r"^detail_class/(?P<id>[0-9]+)/$", Detail.as_view()),
    url(r"^detail_class_explicit/(?P<id>[0-9]+)/$", DetailExplicit.as_view()),
    url(r"^detail_class_reqfmt/(?P<id>[0-9]+)/$", DetailReqFmt.as_view()),
    url(r"^detail_class_manual/(?P<id>[0-9]+)/$", DetailManual.as_view()),
    url(r"^detail_class_manual/$", DetailManual.as_view()),
    url(r"^view_class/", View.as_view()),
    url(r"^view_class_json/", JsonView.as_view()),
    url(r"^", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
