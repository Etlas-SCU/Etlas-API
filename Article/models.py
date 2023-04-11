from django.db import models
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
# Create your models here.





class Articles(models.Model):
    image = models.ImageField(upload_to="articles_images/")
    article_title = models.CharField(max_length=200)
    date = models.DateField()


    def delete(self, *args, **kwargs):
        # Delete the image file from Backblaze B2 bucket
        default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class Section(models.Model):
    article = models.ForeignKey(Articles,on_delete=models.CASCADE)
    section_title = models.CharField(max_length=200)
    description = models.TextField()




@receiver(pre_delete, sender=Articles)
def delete_image(sender, instance, **kwargs):
    """
    Delete the image file from Backblaze B2 bucket when the instance of the model
    is deleted.
    """
    default_storage.delete(instance.image.name)


    