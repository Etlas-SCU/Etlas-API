from django.shortcuts import render
from rest_framework import generics
from .models import Tours,Section,Image
from .serializers import ImageSerializers,ToursSerializers,SectionSerializers
# Create your views here.


class ToursList(generics.ListAPIView):
    queryset = Tours.objects.all()
    serializer_class = ToursSerializers
    search_fields = ['title']




class Sectionlist(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializers


class Imagelist(generics.ListAPIView):
    queryset = Image
    serializer_class = ImageSerializers
    