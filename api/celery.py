from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')
app.conf.enable_utc = False

app.conf.update(timezone='Africa/Cairo')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


# Celery beat settings
app.conf.beat_schedule = {
    "clear-blacklisted-tokens-at-midnight": {
        "task": "authentication.tasks.delete_tokens",
        "schedule": crontab(hour=0, minute=0)
    }, 
    "clear-unverified-users-at-midnight": {
        "task": "users.tasks.clear_unverified_users",
        "schedule": crontab(hour=0, minute=0)
    },
    "refill-scans-left-at-midnight": {
        "task": "users.tasks.refill_scans_left",
        "schedule": crontab(hour=0, minute=0)
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
