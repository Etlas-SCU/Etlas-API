from django.urls import path

from . import views

register = views.RegisterView.as_view({
    'post': 'create',
})

urlpatterns = [
    path('register/', register, name="register"),

]
