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



urlpatterns = [
    path('register/', register, name="register"),
    path('email_verify/', verify, name="email_verify"),
    path('request_verify_otp/', request_verify_otp, name="request_verify_otp"),
    path('login/', login, name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', password_reset, name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckView.as_view(), name="password-reset-confirm"),
    path('password-reset-complete/', views.SetNewPasswordView.as_view(), name="password-reset-complete"),
    path('logout/', logout, name="logout"),
]
