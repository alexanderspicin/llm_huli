from rest_framework import serializers

from llm_huli.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class TextUploadSerializer(serializers.Serializer):
    text = serializers.CharField()
