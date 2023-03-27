from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .tasks import validate_question_task

# Create your models here.

class Choice(models.Model):
    """ Chocie model for the multiple choice questions """
    
    choice_text = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.choice_text


LABEL_CHOICES = (
    ('statue', 'statue'),
    ('monument', 'monument'),
    ('landmark', 'landmark'),
)

class Question(models.Model):
    """ Question model for the multiple choice questions """

    statement = models.CharField(max_length=200)
    label = models.CharField(max_length=200, choices=LABEL_CHOICES)
    image = models.ImageField(upload_to='questions_images/')
    correct_chocie = models.CharField(max_length=200)
    choices = models.ManyToManyField(Choice, related_name='choices')

    def __str__(self):
        return self.statement
    
    def delete(self, *args, **kwargs):
        # Delete the image file from Backblaze B2 bucket
        default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)
    
@receiver(post_save, sender=Question)
def validate_question(sender, instance, created, **kwargs):
    """
    Validate the question after it is created.
    """
    if created:
        validate_question_task.apply_async(args=[instance.id], countdown=10)


@receiver(pre_delete, sender=Question)
def delete_image(sender, instance, **kwargs):
    """
    Delete the image file from Backblaze B2 bucket when the instance of the model
    is deleted.
    """
    default_storage.delete(instance.image.name)
