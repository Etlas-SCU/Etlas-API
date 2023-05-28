from django.contrib import admin

from .models import Favorite


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "monument", "article", "created_at"]
    list_filter = ["user", "monument", "article", "created_at"]
    search_fields = ["user", "monument", "article", "created_at"]

    class Meta:
        model = Favorite


admin.site.register(Favorite, FavoriteAdmin)
