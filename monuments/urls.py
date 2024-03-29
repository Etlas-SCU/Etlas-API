from django.urls import path

from . import views

app_name = "monuments"
urlpatterns = [
    path("", views.MonumentListView.as_view()),
    path("<int:pk>/", views.MonumentDetailView.as_view()),
    path("detect/", views.MonumentDetectionView.as_view()),
]
