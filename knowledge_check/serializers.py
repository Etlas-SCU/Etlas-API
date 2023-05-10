from rest_framework import serializers
import environ, random
from .models import Question

env = environ.Env()

class QuestionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    shuffeld_choices = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.image}'

    def get_shuffeld_choices(self, obj):
        choices = list(obj.choices.values())
        random.shuffle(choices)
        return choices

    class Meta:
        model = Question
        fields = ['id', 'statement', 'image_url', 'label', 'correct_chocie', 'shuffeld_choices']
