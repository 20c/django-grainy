from rest_framework import serializers
from .models import ModelA


class ModelASerializer(serializers.HyperlinkedModelSerializer):

    nested_dict = serializers.SerializerMethodField(required=False)

    class Meta:
        model = ModelA
        fields = ("name", "id", "nested_dict")

    def get_nested_dict(self, obj):
        return {"secret": {"hidden": "data"}, "something": "public"}
