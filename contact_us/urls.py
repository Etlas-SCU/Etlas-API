from django.urls import path

from . import views

urlpatterns = [
    path('message/', views.messageView.as_view(), name="message"),
]
