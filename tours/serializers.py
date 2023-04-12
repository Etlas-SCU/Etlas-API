from rest_framework import serializers
from .models import Tours,Section,Image

class SectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'



class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'



class ToursSerializers(serializers.ModelSerializer):
    section = SectionSerializers(many=True,read_only=True)
    image = ImageSerializers(many=True,read_only=True)
    class Meta:
        model = Tours
        fields = '__all__'
        depth = 1


