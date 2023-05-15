from django.urls import path

from . import views

app_name = "monuments"
urlpatterns = [
    path("", views.MonumentListView.as_view()),
]
