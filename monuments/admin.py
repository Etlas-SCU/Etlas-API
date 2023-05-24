from django.contrib import admin

from .models import Monument


class MonumentAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "updated")
    list_filter = ["created"]
    search_fields = ["name"]
    readonly_fields = ["created", "updated"]


admin.site.register(Monument, MonumentAdmin)