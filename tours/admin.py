from django.contrib import admin
from .models import Tour, TourSection, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class TourSectionInline(admin.TabularInline):
    model = TourSection
    extra = 1


class TourAdmin(admin.ModelAdmin):
    inlines = [TourSectionInline, ImageInline]


admin.site.register(Tour, TourAdmin)
admin.site.register(TourSection)
admin.site.register(Image)
