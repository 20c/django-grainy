from django.conf.urls import url, include
from rest_framework import routers
from .views import (
    ModelAViewSet,
    JsonView,
    View,
    view
)

router = routers.DefaultRouter()
router.register(r'a', ModelAViewSet)


urlpatterns = [
    url(r'^view/', view),
    url(r'^view_class/', View.as_view()),
    url(r'^view_class_json/', JsonView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
