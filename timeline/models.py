import math

from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class HistoryTimeline(models.Model):
    """ HistoryTimeline model for timeline app """
    timeline_name = models.CharField(max_length=200)
    timeline_start = models.IntegerField(default=-math.inf)
    timeline_end = models.IntegerField(default=math.inf)
    timeline_description = models.TextField(default="")

    def __str__(self):
        return self.timeline_name

    class Meta:
        ordering = ('timeline_start',)


class Era(models.Model):
    """ Era model for timeline app """
    era_name = models.CharField(max_length=200)
    era_start = models.IntegerField(default=-math.inf)
    era_end = models.IntegerField(default=math.inf)
    era_description = models.TextField(default="")
    history_timeline = models.ForeignKey(HistoryTimeline, on_delete=models.CASCADE, related_name='eras')
    image = models.ImageField(upload_to='era_images', blank=True, null=True)

    def __str__(self):
        return self.era_name


@receiver(pre_delete, sender=Era)
def delete_era_image(sender, instance, **kwargs):
    """ Deletes image file from filesystem when corresponding `Era` object is deleted. """
    if instance.image:
        path = instance.image.path
        default_storage.delete(path)
