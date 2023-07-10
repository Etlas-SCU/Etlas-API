import environ
import stripe
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserPayment

env = environ.Env()

stripe.api_key = env('STRIPE_SECRET_KEY')
endpoint_secret = env('WEBHOOK_SECRET_KEY')


class StripeWebhook(views.APIView):
    def post(self, request, *args, **kwargs):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response(status=400)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            user_payment = UserPayment.objects.get(stripe_checkout_id=session['id'])
            user_payment.payment_bool = True
            user_payment.save()
            user = user_payment.app_user
            user.scans_left = 5

        return Response(status=200)


class UserPaidView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = UserPayment.objects.get(app_user=request.user)
        return Response({'payment_bool': user.payment_bool})