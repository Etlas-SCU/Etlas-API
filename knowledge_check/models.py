from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage

# Create your models here.

class Choice(models.Model):
    """ Chocie model for the multiple choice questions """
    
    choice_text = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.choice_text

class Question(models.Model):
    """ Question model for the multiple choice questions """

    statement = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    image = models.ImageField(upload_to='questions_images/')
    correct_chocie = models.CharField(max_length=200)
    choices = models.ManyToManyField(Choice, related_name='choices')

    def __str__(self):
        return self.statement
    
    def delete(self, *args, **kwargs):
        # Delete the image file from Backblaze B2 bucket
        default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)
    
@receiver(pre_delete, sender=Question)
def delete_image(sender, instance, **kwargs):
    """
    Delete the image file from Backblaze B2 bucket when the instance of the model
    is deleted.
    """
    default_storage.delete(instance.image.name)
