from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

register = views.RegisterView.as_view({
    'post': 'create',
})

verify = views.VerifyEmailView.as_view({
    'get': 'retrieve',
})

login = views.LoginView.as_view({
    'post': 'create',
})

urlpatterns = [
    path('register/', register, name="register"),
    path('email_verify/', verify, name="email_verify"),
    path('login/', login, name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
