from rest_framework.serializers import ModelSerializer
from .models import message

class MessageSerializer(ModelSerializer):
    class Meta:
        model = message
        fields = '__all__'
