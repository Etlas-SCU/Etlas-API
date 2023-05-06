from django.shortcuts import render
from rest_framework import generics
from .models import Tour,TourSection,Image
from .serializers import ImageSerializers,TourSerializer,TourSectionSerializer
# Create your views here.


class ToursList(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    search_fields = ['title']


class GetSingleTour(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer





    