from django.db import models
from django_extensions.db.models import TimeStampedModel


class Monument(TimeStampedModel):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
