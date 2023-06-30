from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task(bind=True)
def send_contact_us_email(self, data):
    send_mail(
        subject=data['email_subject'],
        message=data['email_body'],
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )

    return "Sent!"