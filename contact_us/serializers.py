from rest_framework.serializers import ModelSerializer
from .models import message

class messageSerializer(ModelSerializer):
    class Meta:
        model = message
        fields = ['full_name', 'email', 'subject', 'message']
        extra_kwargs = {
            'full_name': {'required': True, 'write_only': True},
            'email': {'required': True, 'write_only': True},
            'subject': {'required': True, 'write_only': True},
            'message': {'required': True, 'write_only': True},
        }
