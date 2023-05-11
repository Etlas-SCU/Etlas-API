from .models import Article,Section
from rest_framework import serializers


    
class SectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id','section_title','description']




class ArticlesSerializers(serializers.ModelSerializer):
    sections = SectionSerializers(many=True,read_only=True)
    class Meta:
        model = Article
        fields = ['id','article_title','date','image','description','sections']
       



