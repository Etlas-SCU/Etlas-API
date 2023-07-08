import environ
from rest_framework import serializers

from .models import Monument

env = environ.Env()


class MonumentSerializer(serializers.ModelSerializer):
    three_d_model = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Monument
        fields = ['id', 'name', 'description', 'created', 'updated', 'three_d_model', 'location', 'date', 'image_url']

    def get_three_d_model(self, obj):
        if obj.model_obj and obj.model_texture:
            return {
                'model_obj': f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.model_obj}',
                'model_texture': f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.model_texture}'
            }
        
        return None
    
    def get_date(self, obj):
        if(obj.date):
            if(obj.date < 0):
                return f"{abs(obj.date)} BC"
            else:
                return f"{obj.date} AD"
        
        return None
    
    def get_image_url(self, obj):
        if obj.image:
            return f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.image}'
        
        return None


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
