from rest_framework import generics

from .models import HistoryTimeline
from .paginators import CustomLimitOffsetPagination
from .serializers import HistoryTimelineSerializer


class HistoryTimelineList(generics.ListAPIView):
    """ List all HistoryTimelines """
    queryset = HistoryTimeline.objects.all()
    serializer_class = HistoryTimelineSerializer
    pagination_class = CustomLimitOffsetPagination


class HistoryTimelineDetail(generics.RetrieveAPIView):
    """ Retrieve a single HistoryTimeline """
    queryset = HistoryTimeline.objects.all()
    serializer_class = HistoryTimelineSerializer
