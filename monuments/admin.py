from django.contrib import admin

from .models import Monument


class MonumentAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    list_filter = ["created_at"]
    search_fields = ["name"]


admin.site.register(Monument, MonumentAdmin)