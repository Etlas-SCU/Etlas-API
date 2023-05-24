from django.contrib import admin

from monuments.admin import ArticleMonumentInline
from .models import Article, Section


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("article_title", "created", "updated", 'get_monuments')
    inlines = [SectionInline, ArticleMonumentInline]

    def get_monuments(self, obj):
        return " - ".join([a.name for a in obj.monuments.all()])

    get_monuments.short_description = 'Monuments'


admin.site.register(Article, ArticleAdmin)
admin.site.register(Section)
