from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')
app.conf.enable_utc = False

app.conf.update(timezone = 'Africa/Cairo')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


# Celery beat settings



@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')