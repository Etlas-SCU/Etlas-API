from django.shortcuts import render
from .models import Article,Section
from .serializers import ArticlesSerializers
from rest_framework import generics
# Create your views here.




class ArticlesList(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticlesSerializers
    search_fields = ['title']
    # ordering_fields = ['date']



class GetSingleArticle(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticlesSerializers




