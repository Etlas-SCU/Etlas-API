from .models import Article
from .serializers import ArticlesSerializers
from rest_framework import generics


class ArticlesList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticlesSerializers
    search_fields = ['title']


class GetSingleArticle(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticlesSerializers
