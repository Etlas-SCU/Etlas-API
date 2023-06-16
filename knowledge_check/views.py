import random

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Question
from .serializers import QuestionSerializer


# Create your views here.

class QuestionStatuesViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(label='statue')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        shuffled = list(serializer.data)
        random.shuffle(shuffled)

        return Response(shuffled)


class QuestionMonumentsViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(label='monument')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        shuffled = list(serializer.data)
        random.shuffle(shuffled)

        return Response(shuffled)


class QuestionLandmarksViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(label='landmark')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        shuffled = list(serializer.data)
        random.shuffle(shuffled)

        return Response(shuffled)
