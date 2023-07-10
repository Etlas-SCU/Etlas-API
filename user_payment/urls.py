from django.urls import path

from . import views

app_name = 'user_payment'
urlpatterns = [
    path('stripe-webhook/', views.StripeWebhook.as_view(), name='stripe_webhook'),
    path('user-paid/', views.UserPaidView.as_view(), name='user_paid'),
]
