from rest_framework import serializers

from articles.serializers import ArticleSerializer
from monuments.serializers import MonumentSerializer
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    monument = MonumentSerializer(read_only=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'monument', 'article', 'created_at']
        read_only_fields = ["id", "user", "created_at"]


class FavoriteCreateDestroySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        fields = ['id']


class IsFavoriteSerializer(serializers.Serializer):
    monument_id = serializers.IntegerField(required=False)
    article_id = serializers.IntegerField(required=False)

    class Meta:
        fields = ['monument_id', 'article_id']
