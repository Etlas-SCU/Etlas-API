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
        if obj.era_end == math.inf:
            return "After Time"
        if obj.era_end < 0:
            return f"{abs(obj.era_end)} BC"
        else:
            return f"{obj.era_end} AD"

    def get_start_date(self, obj):
        if obj.era_start == -math.inf:
            return "Before Time"
        if obj.era_start < 0:
            return f"{abs(obj.era_start)} BC"
        else:
            return f"{obj.era_start} AD"

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
        if obj.timeline_end == math.inf:
            return "After Time"
        if obj.timeline_end < 0:
            return f"{abs(obj.timeline_end)} BC"
        else:
            return f"{obj.timeline_end} AD"

    def get_start_date(self, obj):
        if obj.timeline_start == -math.inf:
            return "Before Time"
        if obj.timeline_start < 0:
            return f"{abs(obj.timeline_start)} BC"
        else:
            return f"{obj.timeline_start} AD"

    get_start_date.short_description = 'Start Date'
    get_end_date.short_description = 'End Date'


admin.site.register(HistoryTimeline, HistoryTimelineAdmin)
admin.site.register(Era, EraAdmin)
