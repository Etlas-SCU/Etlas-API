from rest_framework import serializers

from .models import Monument


class MonumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monument
        fields = ['id', 'name', 'description', 'created', 'updated']


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
