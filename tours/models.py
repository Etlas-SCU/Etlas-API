from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Tour(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class TourSection(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tours = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.title


class Image(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="tours_images/")

    def delete(self, *args, **kwargs):
        # Delete the image file from Backblaze B2 bucket
        default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)


@receiver(pre_delete, sender=Tour)
def delete_image(sender, instance, **kwargs):
    """
    Delete the image file from Backblaze B2 bucket when the instance of the model
    is deleted.
    """
    default_storage.delete(instance.image.name)
