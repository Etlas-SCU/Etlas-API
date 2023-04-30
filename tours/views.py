from django.shortcuts import render
from rest_framework import generics
from .models import Tours,Section,Image
from .serializers import ImageSerializers,ToursSerializers,TourSectionSerializers
# Create your views here.


class ToursList(generics.ListAPIView):
    queryset = Tours.objects.all()
    serializer_class = ToursSerializers
    search_fields = ['title']


class GetSingleTour(generics.RetrieveAPIView):
    queryset = Tours.objects.all()
    serializer_class = ToursSerializers





class Sectionlist(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = TourSectionSerializers


class Imagelist(generics.ListAPIView):
    queryset = Image
    serializer_class = ImageSerializers
    