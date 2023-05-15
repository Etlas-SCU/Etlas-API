from django.urls import path

from . import views

urlpatterns = [
    path("", views.MonumentListView.as_view()),
]
