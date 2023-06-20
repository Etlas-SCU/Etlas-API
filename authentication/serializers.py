import environ
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.models import User

env = environ.Env()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, min_length=8, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=255, min_length=8, write_only=True, required=True)
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{obj.image}'
        else:
            return None

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

        user = User.objects.create_user(email=email, full_name=full_name, address=address, phone_number=phone_number,
                                        image=image, password=password)

        return user

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password', 'confirm_password', 'address', 'phone_number', 'image_url']


class EmailVerficationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=4, min_length=4, write_only=True, required=True)

    class Meta:
        fields = ['otp']


class ResendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2, required=True)

    class Meta:
        fields = ['email']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)
    image_url = serializers.SerializerMethodField()
    tokens = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        user = User.objects.get(email=obj['email'])
        if user.image:
            return f'https://{env("AWS_STORAGE_BUCKET_NAME")}.s3.{env("AWS_S3_REGION_NAME")}.backblazeb2.com/media/{user.image}'
        else:
            return None

    def get_tokens(self, obj):

        user = User.objects.get(email=obj['email'])

        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
        }

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'full_name', 'address', 'phone_number', 'image_url', 'tokens']
        extra_kwargs = {
            'address': {'read_only': True},
            'phone_number': {'read_only': True},
            'image_url': {'read_only': True},
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

        if not filtered_user_by_email.exists():
            raise AuthenticationFailed('The email is not registered')

        if not user:
            raise AuthenticationFailed('Invalid password, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
        }


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=255, write_only=True, required=True)
    confirm_password = serializers.CharField(min_length=8, max_length=255, write_only=True, required=True)
    token = serializers.CharField(min_length=1, write_only=True, required=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True, required=True)

    class Meta:
        fields = ['password', 'confirm_password', 'token', 'uidb64']

    def validate(self, attrs):

        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

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
