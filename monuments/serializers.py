from rest_framework import serializers

from .models import Monument


class MonumentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Monument
        fields = ['id', 'name', 'created_at', 'updated_at']
