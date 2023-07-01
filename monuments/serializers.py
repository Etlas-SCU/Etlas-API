import environ
from rest_framework import serializers

from .models import Monument

env = environ.Env()


class MonumentSerializer(serializers.ModelSerializer):
    three_d_model = serializers.SerializerMethodField()

    class Meta:
        model = Monument
        fields = ['id', 'name', 'description', 'created', 'updated', 'three_d_model']

    def get_three_d_model(self, obj):
        if obj.model_obj and obj.model_texture:
            return {
                'model_obj': f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.model_obj}',
                'model_texture': f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.model_texture}'
            }


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
