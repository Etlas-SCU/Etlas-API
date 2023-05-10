from rest_framework import serializers
from .models import HistoryTimeline, Era


class EraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Era
        fields = ['id', 'era_name', 'era_start', 'era_end', 'era_description', 'image']


class HistoryTimelineSerializer(serializers.ModelSerializer):
    eras = EraSerializer(many=True, read_only=True)

    class Meta:
        model = HistoryTimeline
        fields = ['id', 'timeline_name', 'timeline_start', 'timeline_end', 'timeline_description', 'eras']
