from rest_framework import generics

from .models import Article
from .serializers import ArticleSerializer


class ArticlesList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    search_fields = ['title']


class GetSingleArticle(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
