from django.db import models
from django_extensions.db.models import TimeStampedModel


class Monument(TimeStampedModel):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    # texture, and obj model
    model_texture = models.ImageField(upload_to="monuments_images/", blank=True, null=True, verbose_name="Texture",
                                      help_text="Upload a .png file")
    model_obj = models.FileField(upload_to="monuments_obj/", blank=True, null=True, verbose_name="Model",
                                 help_text="Upload a .obj file")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-updated',)


class ArticleMonument(models.Model):
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, related_name="article_monuments",
                                blank=True)
    monument = models.ForeignKey("monuments.Monument", on_delete=models.CASCADE, related_name="article_monuments",
                                 blank=True)

    def __str__(self):
        return f"{self.article.article_title} - {self.monument.name}"
