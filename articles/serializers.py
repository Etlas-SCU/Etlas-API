import environ
from rest_framework import serializers

from monuments.models import ArticleMonument
from monuments.serializers import MonumentSerializer
from .models import Article, Section

env = environ.Env()


class SectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'section_title', 'description']


class ArticleSerializer(serializers.ModelSerializer):
    sections = SectionSerializers(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    monuments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'article_title', 'date', 'image_url', 'description', 'sections', 'monuments']

    def get_image_url(self, obj):
        if obj.image:
            return f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.image}'
        return None

    def get_monuments(self, obj):
        article_monument_interface = ArticleMonument.objects.filter(article=obj)
        monuments_list = map(lambda x: x.monument, article_monument_interface)
        serializer = MonumentSerializer(monuments_list, many=True)
        return serializer.data
