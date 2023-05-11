from django.contrib import admin
from .models import Article,Section
# Register your models here.

class SectionInline(admin.TabularInline):
    model=Section
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    inlines = [SectionInline]


admin.site.register(Article,ArticleAdmin)
admin.site.register(Section)

