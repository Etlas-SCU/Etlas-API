from django.db import models
from django_extensions.db.models import TimeStampedModel


class Monument(TimeStampedModel):
    name = models.CharField(max_length=100)
