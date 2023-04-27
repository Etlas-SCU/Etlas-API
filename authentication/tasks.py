from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True)
def verification_mail(self, data):
    send_mail(
        subject = data['email_subject'],
        message= data['email_body'],
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list=[data['to_email'], ],
        fail_silently= False,
    )

    return "Sent!"
