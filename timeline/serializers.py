from rest_framework import serializers
from .models import HistoryTimeline, Era


class EraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Era
        fields = ['id', 'era_name', 'era_start', 'era_end', 'era_description', 'image']


class HistoryTimelineSerializer(serializers.ModelSerializer):
    eras = serializers.SerializerMethodField()

    class Meta:
        model = HistoryTimeline
        fields = ['id', 'timeline_name', 'timeline_start', 'timeline_end', 'timeline_description', 'eras']

    def get_eras(self, obj):
        eras = Era.objects.filter(history_timeline=obj)
        serializer = EraSerializer(eras, many=True)
        return serializer.data
