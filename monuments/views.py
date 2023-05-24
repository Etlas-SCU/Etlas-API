from rest_framework import generics

from monuments.models import Monument
from monuments.serializers import MonumentSerializers


class MonumentListView(generics.ListAPIView):
    """ List all Monuments """
    queryset = Monument.objects.all()
    serializer_class = MonumentSerializers


class MonumentDetailView(generics.RetrieveAPIView):
    """ Retrieve a single Monument """
    queryset = Monument.objects.all()
    serializer_class = MonumentSerializers
