from celery import shared_task
from users.models import User
from django.utils import timezone

@shared_task(bind=True)
def clear_unverified_users(self):
    users = User.objects.filter(is_verified=False)
    time = timezone.now() 
    for user in users:
        if (time - user.created_at).days >= 30:
            user.delete()

    return "Deleted unverified users!"
