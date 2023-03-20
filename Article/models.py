from django.db import models

# Create your models here.

class Section(models.Model):
    section_title = models.CharField(max_length=200)
    description = models.TextField()



class Articles(models.Model):
    section = models.ForeignKey(Section,on_delete=models.CASCADE,null=True)
    article_title = models.CharField(max_length=200)
    date = models.DateField()
