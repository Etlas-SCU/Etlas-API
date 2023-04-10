from .models import Articles
from rest_framework import serializers




class ArticlesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['id',"image",'article_title','date','section']
        depth = 1

        