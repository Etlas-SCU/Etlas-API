from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.utils import timezone


@shared_task(bind=True)
def send_email(self, data):
    send_mail(
        subject=data['email_subject'],
        message=data['email_body'],
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[data['to_email'], ],
        fail_silently=False,
    )

    return "Sent!"

@shared_task(bind=True)
def delete_tokens(self):
    BlacklistedToken.objects.filter(token__expires_at__lt=timezone.now()).delete()
    OutstandingToken.objects.filter(expires_at__lt=timezone.now()).delete()
    return "Deleted!"
