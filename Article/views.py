from django.shortcuts import render
from .models import Articles
from .serializers import ArticlesSerializers
from rest_framework import generics
# Create your views here.

class ArticlesList(generics.ListAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializers
    search_fields = ['title']
    # ordering_fields = ['date']



class GetSingleArticle(generics.RetrieveAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializers

    




