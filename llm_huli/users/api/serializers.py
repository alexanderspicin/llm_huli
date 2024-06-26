from rest_framework import serializers

from llm_huli.users.models import User, File


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class TextUploadSerializer(serializers.Serializer):
    text = serializers.CharField()

class TextFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        print(value.content_type)
        if value.content_type != 'text/plain':
            raise serializers.ValidationError('Only .txt files are allowed.')
        return value

class TextFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'uploaded_at')
