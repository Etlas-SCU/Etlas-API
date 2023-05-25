from rest_framework import serializers

from articles.serializers import ArticleSerializer
from monuments.serializers import MonumentSerializer
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    get_monument = MonumentSerializer(read_only=True)
    get_article = ArticleSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'get_monument', 'get_article', 'created_at']
        read_only_fields = ["id", "user", "created_at"]
