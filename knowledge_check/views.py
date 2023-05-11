from rest_framework import viewsets

from .models import Question
from .serializers import QuestionSerializer

# Create your views here.

class QuestionStatuesViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(label='statue')
    serializer_class = QuestionSerializer

class QuestionMonumentsViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(label='monument')
    serializer_class = QuestionSerializer

class QuestionLandmarksViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(label='landmark')
    serializer_class = QuestionSerializer
