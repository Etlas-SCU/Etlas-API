from rest_framework import serializers

from .models import Monument


class MonumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monument
        fields = ['id', 'name', 'created', 'updated']
