from rest_framework import serializers
from users.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

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

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):

        user = User.objects.get(email = obj['email'])

        return{
            'access' : user.tokens()['access'],
            'refresh' : user.tokens()['refresh'],
        }
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'full_name', 'address', 'phone_number', 'image', 'best_score', 'tokens']
        extra_kwargs = {
            'best_score': {'read_only': True},
            'address': {'read_only': True},
            'phone_number': {'read_only': True},
            'image': {'read_only': True},
            'full_name': {'read_only': True},
        }


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)


        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        return {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'address': user.address,
            'phone_number': user.phone_number,
            'image': user.image,
            'best_score': user.best_score,
            'tokens': user.tokens
        }


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=255, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }
    
    def validate(self, data):
        self.token = data['refresh']

        return data
    
    def save(self, **kwargs):
        try: 
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
