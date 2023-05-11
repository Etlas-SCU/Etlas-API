import math

from rest_framework import serializers
from .models import HistoryTimeline, Era


class EraSerializer(serializers.ModelSerializer):
    era_start_date = serializers.SerializerMethodField()
    era_end_date = serializers.SerializerMethodField()

    class Meta:
        model = Era
        fields = ['id', 'era_name', 'era_start_date', 'era_end_date', 'era_description', 'image']

    def get_era_start_date(self, obj):
        if obj.era_start == -math.inf:
            return "Before Time"
        if obj.era_start < 0:
            return f"{abs(obj.era_start)} BC"
        else:
            return f"{obj.era_start} AD"

    def get_era_end_date(self, obj):
        if obj.era_end == math.inf:
            return "After Time"
        if obj.era_end < 0:
            return f"{abs(obj.era_end)} BC"
        else:
            return f"{obj.era_end} AD"


class HistoryTimelineSerializer(serializers.ModelSerializer):
    eras = EraSerializer(many=True, read_only=True)
    timeline_start_date = serializers.SerializerMethodField()
    timeline_end_date = serializers.SerializerMethodField()

    class Meta:
        model = HistoryTimeline
        fields = ['id', 'timeline_name', 'timeline_start_date', 'timeline_end_date', 'timeline_description', 'eras']

    def get_timeline_start_date(self, obj):
        if obj.timeline_start == -math.inf:
            return "Before Time"
        if obj.timeline_start < 0:
            return f"{abs(obj.timeline_start)} BC"
        else:
            return f"{obj.timeline_start} AD"

    def get_timeline_end_date(self, obj):
        if obj.timeline_end == math.inf:
            return "After Time"
        if obj.timeline_end < 0:
            return f"{abs(obj.timeline_end)} BC"
        else:
            return f"{obj.timeline_end} AD"
