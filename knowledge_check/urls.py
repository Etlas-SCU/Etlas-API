from django.urls import path

from .views import QuestionStatuesViewSet, QuestionMonumentsViewSet, QuestionLandmarksViewSet

questions_statues = QuestionStatuesViewSet.as_view({
    'get': 'list',
})

questions_monuments = QuestionMonumentsViewSet.as_view({
    'get': 'list',
})

questions_landmarks = QuestionLandmarksViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    path('questions/statues', questions_statues, name='questions_statues'),
    path('questions/monuments', questions_monuments, name='questions_monuments'),
    path('questions/landmarks', questions_landmarks, name='questions_landmarks'),
]
