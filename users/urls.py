from django.urls import path

from . import views

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

total_best_score = views.TotalBestScoreView.as_view({
    'get': 'retrieve',
})

best_score_statues = views.BestScoreStatuesView.as_view({
    'get': 'retrieve',
    'put': 'update',
})

best_score_landmarks = views.BestScoreLandmarksView.as_view({
    'get': 'retrieve',
    'put': 'update',
})

best_score_monuments = views.BestScoreMonumentsView.as_view({
    'get': 'retrieve',
    'put': 'update',
})

urlpatterns = [
    path('', user_detail, name="user-detail"),
    path('total-best-score/', total_best_score, name="total-best-score"),
    path('best-score-statues/', best_score_statues, name="best-score-statues"),
    path('best-score-landmarks/', best_score_landmarks, name="best-score-landmarks"),
    path('best-score-monuments/', best_score_monuments, name="best-score-monuments"),
    path('profile-image/', views.ChangeImageView.as_view(), name='profile-image'),
]
