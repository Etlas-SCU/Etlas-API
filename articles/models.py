from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel

from monuments.models import Monument


class Article(TimeStampedModel):
    article_title = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to="articles_images/")
    description = models.TextField()
    monuments = models.ManyToManyField(Monument, related_name='articles', blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article_title

    def delete(self, *args, **kwargs):
        # Delete the image file from Backblaze B2 bucket
        default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ('-updated',)


class Section(models.Model):
    article = models.ForeignKey(Article, related_name='sections', on_delete=models.CASCADE)
    section_title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.section_title


@receiver(pre_delete, sender=Article)
def delete_image(sender, instance, **kwargs):
    """
    Delete the image file from Backblaze B2 bucket when the instance of the model
    is deleted.
    """
    default_storage.delete(instance.image.name)
