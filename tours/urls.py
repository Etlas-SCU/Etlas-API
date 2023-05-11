from django.urls import path
from . import views

urlpatterns = [
    path("", views.ToursList.as_view()),
    path("<int:pk>/", views.GetSingleTour.as_view())
]
