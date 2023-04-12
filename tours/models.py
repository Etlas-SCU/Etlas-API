from django.db import models

# Create your models here.


class Tours(models.Model):
    title = models.CharField(max_length=200)
    rating = models.SmallIntegerField()



class Section(models.Model):
    tour = models.ForeignKey(Tours,on_delete=models.CASCADE)
    section_title = models.CharField(max_length=200)
    description = models.TextField()


class Image(models.Model):
    tour = models.ForeignKey(Tours,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tours_images/")


