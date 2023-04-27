from django.urls import path

from . import views

register = views.RegisterView.as_view({
    'post': 'create',
})

verify = views.VerifyEmailView.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path('register/', register, name="register"),
    path('email_verify', verify, name="email_verify"),
]
