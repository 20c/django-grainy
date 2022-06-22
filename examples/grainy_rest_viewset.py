from rest_framework import serializers

from django_grainy.decorators import grainy_rest_viewset

from .models import TestModelA


# A serializer to test with
class ModelASerializer(serializers.HyperlinkedModelSerializer):

    # to test applying of permissions in nested data
    nested_dict = serializers.SerializerMethodField(required=False)

    class Meta:
        model = TestModelA
        fields = ("name", "id", "nested_dict")

    def get_nested_dict(self, obj):
        return {"secret": {"hidden": "data"}, "something": "public"}


@grainy_rest_viewset(
    namespace="api.a",
    handlers={
        # with application handlers we can tell grainy that this
        # namespace needs to have explicit permissions in order
        # to be accessed
        "nested_dict.secret": {"explicit": True}
    },
)
class ModelAViewSet(viewsets.ModelViewSet):
    queryset = TestModelA.objects.all()
    serializer_class = ModelASerializer
