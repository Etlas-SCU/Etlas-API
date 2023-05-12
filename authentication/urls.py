from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

register = views.RegisterView.as_view({
    'post': 'create',
})

verify = views.VerifyEmailView.as_view({
    'post': 'create',
})

request_verify_otp = views.RequestAnotherVerificationOTPView.as_view({
    'post': 'create',
})

login = views.LoginView.as_view({
    'post': 'create',
})

password_reset = views.RequestPasswordResetEmailView.as_view({
    'post': 'create',
})

logout = views.LogoutView.as_view({
    'post': 'create',
})

password_reset_otp = views.CheckResetPasswordOTPView.as_view({
    'post': 'create',
})

urlpatterns = [
    path('register/', register, name="register"),
    path('email-verify/', verify, name="email-verify"),
    path('request-verify-otp/', request_verify_otp, name="request-verify-otp"),
    path('login/', login, name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-password-reset/', password_reset, name="request-password-reset"),
    path('password-reset-otp/', password_reset_otp, name="password-reset-otp"),
    path('password-reset-complete/', views.SetNewPasswordView.as_view(), name="password-reset-complete"),
    path('logout/', logout, name="logout"),
]
