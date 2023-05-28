from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    monument = models.ForeignKey("monuments.Monument", on_delete=models.CASCADE, null=True, blank=True,
                                 related_name="monument")
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, null=True, blank=True,
                                related_name="article")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "monument", "article"]

    def __str__(self):
        return f"{self.user} - {self.monument} - {self.article}"
