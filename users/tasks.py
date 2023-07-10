from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task(bind=True)
def clear_unverified_users(self):
    users = User.objects.filter(is_verified=False)
    time = timezone.now()
    for user in users:
        if (time - user.created_at).days >= 30:
            user.delete()

    return "Deleted unverified users!"


@shared_task(bind=True)
def refill_scans_left(self):
    users = User.objects.all()
    users.update(scans_left=5)

    return "Refilled scans left!"
