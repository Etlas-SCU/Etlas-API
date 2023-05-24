from django.contrib import admin

from .models import Monument, ArticleMonument


class ArticleMonumentInline(admin.StackedInline):
    model = ArticleMonument
    extra = 1


class MonumentAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "updated", 'get_articles')
    list_filter = ["created"]
    search_fields = ["name"]
    readonly_fields = ["created", "updated"]
    inlines = [ArticleMonumentInline]

    def get_articles(self, obj):
        return " - ".join([a.article_title for a in obj.articles.all()])

    get_articles.short_description = 'Articles'


admin.site.register(Monument, MonumentAdmin)
