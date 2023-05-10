import math

from django.db import models


class HistoryTimeline(models.Model):
    """ HistoryTimeline model for timeline app """
    timeline_name = models.CharField(max_length=200)
    timeline_start = models.IntegerField(default=-math.inf)
    timeline_end = models.IntegerField(default=math.inf)
    timeline_description = models.TextField(default="")

    def __str__(self):
        return self.timeline_name


class Era(models.Model):
    """ Era model for timeline app """
    era_name = models.CharField(max_length=200)
    era_start = models.IntegerField(default=-math.inf)
    era_end = models.IntegerField(default=math.inf)
    era_description = models.TextField(default="")
    history_timeline = models.ForeignKey(HistoryTimeline, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='era_images/', blank=True, null=True)

    def __str__(self):
        return self.era_name
