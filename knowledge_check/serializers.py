import random

import environ
from rest_framework import serializers

from .models import Question

env = environ.Env()


class QuestionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    shuffled_choices = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.image}'

    def get_shuffled_choices(self, obj):
        choices = list(obj.choices.values())
        random.shuffle(choices)
        return choices

    class Meta:
        model = Question
        fields = ['id', 'statement', 'image_url', 'label', 'correct_choice', 'shuffled_choices']
