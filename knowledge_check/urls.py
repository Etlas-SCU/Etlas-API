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
    path('statues/', questions_statues, name='questions_statues'),
    path('monuments/', questions_monuments, name='questions_monuments'),
    path('landmarks/', questions_landmarks, name='questions_landmarks'),
]
