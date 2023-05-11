from django.urls import path

from . import views

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
}) 

urlpatterns = [
    path('<int:pk>/', user_detail, name= "user detail"),
]
