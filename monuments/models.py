from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.core.files.storage import default_storage
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Monument(TimeStampedModel):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    # texture, and obj model
    model_texture = models.ImageField(upload_to="monuments_images/", blank=True, null=True, verbose_name="Texture",
                                      help_text="Upload a .png file")
    model_obj = models.FileField(upload_to="monuments_obj/", blank=True, null=True, verbose_name="Model",
                                 help_text="Upload a .obj file")
    
    location = models.CharField(max_length=100, blank=True, null=True)
    
    date = models.IntegerField(blank=True, null=True)

    image = models.ImageField(upload_to="monuments_images/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-updated',)

    def delete(self, *args, **kwargs):
        # Delete the image file from Backblaze B2 bucket
        default_storage.delete(self.image.name)
        default_storage.delete(self.model_texture.name)
        default_storage.delete(self.model_obj.name)
        super().delete(*args, **kwargs)


class ArticleMonument(models.Model):
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, related_name="article_monuments",
                                blank=True)
    monument = models.ForeignKey("monuments.Monument", on_delete=models.CASCADE, related_name="article_monuments",
                                 blank=True)

    def __str__(self):
        return f"{self.article.article_title} - {self.monument.name}"


@receiver(pre_delete, sender=Monument)
def delete_image(sender, instance, **kwargs):
    """
    Delete the image file from Backblaze B2 bucket when the instance of the model
    is deleted.
    """
    default_storage.delete(instance.image.name)
    default_storage.delete(instance.model_texture.name)
    default_storage.delete(instance.model_obj.name)
