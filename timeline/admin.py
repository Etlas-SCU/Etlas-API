import math

from django.contrib import admin

from .models import HistoryTimeline, Era


class EraInline(admin.TabularInline):
    model = Era
    extra = 3


class EraAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['era_name']}),
        ('Date Information', {'fields': ['era_start', 'era_end']}),
        ('Era Description', {'fields': ['era_description']}),
        ('Era Image', {'fields': ['image']}),
    ]
    list_display = ['era_name', 'get_start_date', 'get_end_date']
    list_filter = ['era_start']
    search_fields = ['era_name']

    def get_end_date(self, obj):
        if obj.end_date == math.inf:
            return "After Time"
        if obj.end_date < 0:
            return f"{abs(obj.end_date)} BC"
        else:
            return f"{obj.end_date} AD"

    def get_start_date(self, obj):
        if obj.start_date == -math.inf:
            return "Before Time"
        if obj.start_date < 0:
            return f"{abs(obj.start_date)} BC"
        else:
            return f"{obj.start_date} AD"

    get_start_date.short_description = 'Start Date'
    get_end_date.short_description = 'End Date'


class HistoryTimelineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['timeline_name']}),
        ('Date Information', {'fields': ['timeline_start', 'timeline_end']}),
        ('Timeline Description', {'fields': ['timeline_description']}),
    ]
    inlines = [EraInline]
    list_display = ['timeline_name', 'get_start_date', 'get_end_date']
    list_filter = ['timeline_start']
    search_fields = ['timeline_name']

    def get_end_date(self, obj):
        if obj.end_date == math.inf:
            return "After Time"
        if obj.end_date < 0:
            return f"{abs(obj.end_date)} BC"
        else:
            return f"{obj.end_date} AD"

    def get_start_date(self, obj):
        if obj.start_date == -math.inf:
            return "Before Time"
        if obj.start_date < 0:
            return f"{abs(obj.start_date)} BC"
        else:
            return f"{obj.start_date} AD"

    get_start_date.short_description = 'Start Date'
    get_end_date.short_description = 'End Date'


admin.site.register(HistoryTimeline, HistoryTimelineAdmin)
admin.site.register(Era, EraAdmin)
