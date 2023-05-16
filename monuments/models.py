from django.db import models


class Monument(models.Model):
    name = models.CharField(max_length=100)
