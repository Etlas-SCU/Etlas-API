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
        fields = ['id', 'full_name', 'email', 'address', 'phone_number', 'image_url']


class BestScoreSerializer(serializers.ModelSerializer):
    new_score = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['new_score']


class ImageUpdateSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.image}'
        else:
            return None

    class Meta:
        model = User
        fields = ['image', 'image_url']
        extra_kwargs = {
            'image': {'write_only': True}
        }

    def update(self, instance, validated_data):
        instance.image.delete()
        instance.image = validated_data.get('image', None)
        instance.save()
        return instance
