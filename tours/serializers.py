from rest_framework import serializers
from .models import Tour, TourSection, Image


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


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
