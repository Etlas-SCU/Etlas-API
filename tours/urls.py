from django.urls import path
from . import views

urlpatterns = [
    path("tours/",views.ToursList.as_view()),
    path("tours/<int:pk>",views.GetSingleTour.as_view())
]