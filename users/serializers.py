from rest_framework.serializers import ModelSerializer

from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'address', 'phone_number', 'image', 'best_score']
