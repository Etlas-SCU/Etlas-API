from .models import Articles,Section
from rest_framework import serializers


    
class SectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'




class ArticlesSerializers(serializers.ModelSerializer):
    section = SectionSerializers(many=True,read_only=True)
    class Meta:
        model = Articles
        fields = '__all__'
        depth = 1



