from rest_framework import generics

from .models import Tour
from .serializers import TourSerializer


class ToursList(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    search_fields = ['title']


class GetSingleTour(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
