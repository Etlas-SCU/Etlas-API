from rest_framework import serializers
from users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, min_length=8, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=255, min_length=8, write_only=True, required=True)

    def validate(self, data):
        
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        
        return data
    
    def create(self, validated_data):
        full_name = validated_data.get('full_name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        address = validated_data.get('address')
        phone_number = validated_data.get('phone_number')
        image = validated_data.get('image')

        user = User.objects.create_user(email=email, full_name=full_name, address=address, phone_number=phone_number, image=image, password=password)

        return user
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password', 'confirm_password', 'address', 'phone_number', 'image', 'best_score']
        extra_kwargs = {
            'best_score': {'read_only': True},
        }
        

class EmailVerficationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['token']
