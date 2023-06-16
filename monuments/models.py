from django.db import models
from django_extensions.db.models import TimeStampedModel


class Monument(TimeStampedModel):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-updated', )


class ArticleMonument(models.Model):
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, related_name="article_monuments",
                                blank=True)
    monument = models.ForeignKey("monuments.Monument", on_delete=models.CASCADE, related_name="article_monuments",
                                 blank=True)

    def __str__(self):
        return f"{self.article.article_title} - {self.monument.name}"
