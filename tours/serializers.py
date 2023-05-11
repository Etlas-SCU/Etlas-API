from rest_framework import serializers
from .models import Tour, TourSection, Image

import environ

env = environ.Env()


class ImageSerializers(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.image}'
        return None


class TourSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourSection
        fields = ['id', 'title', 'description']


class TourSerializer(serializers.ModelSerializer):
    sections = TourSectionSerializer(many=True, read_only=True)
    images = ImageSerializers(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = ['id', 'title', 'description', 'sections', 'images']
