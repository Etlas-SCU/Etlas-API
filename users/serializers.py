import environ
from rest_framework import serializers

from .models import User

env = environ.Env()


class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.image}'
        else:
            return None

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'address', 'phone_number', 'image_url', 'best_score']
