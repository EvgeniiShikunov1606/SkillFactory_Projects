from rest_framework import serializers
from .models import Ad, Response


class AdSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Ad
        fields = "__all__"


class ResponseSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Response
        fields = "__all__"

