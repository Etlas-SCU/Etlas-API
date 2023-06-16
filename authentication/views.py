import datetime
import random

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import OTP, User
from .serializers import (EmailVerficationSerializer, LoginSerializer,
                          LogoutSerializer, RegisterSerializer,
                          RequestPasswordResetEmailSerializer,
                          ResendEmailVerificationSerializer,
                          SetNewPasswordSerializer)
from .tasks import send_email


# Create your views here.

class RegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        otp = OTP.objects.create(user=user, otp=random.randint(1000, 9999))
        otp.save()

        email_body = 'Hi ' + user.full_name + \
                     ' Use the OTP below to verify your email \n' + str(otp.otp)
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        send_email.delay(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmailVerficationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data['otp']
        try:
            main_otp = OTP.objects.get(otp=otp)
            user = main_otp.user
            if user.is_verified:
                return Response({'error': 'User already verified'}, status=status.HTTP_400_BAD_REQUEST)

            time = user.otp.created_at + datetime.timedelta(minutes=1)
            current = timezone.now()
            if current > time:
                return Response({'error': 'OTP expired, request another one'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.is_verified = True
                user.otp.delete()
                user.save()

                return Response({'success': 'User verified successfully'}, status=status.HTTP_200_OK)

        except (ValueError, User.DoesNotExist, OTP.DoesNotExist):
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class RequestAnotherVerificationOTPView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ResendEmailVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({'error': 'User already verified'}, status=status.HTTP_400_BAD_REQUEST)
            if hasattr(user, 'otp'):
                user.otp.delete()
                user.save()
            otp = OTP.objects.create(user=user, otp=random.randint(1000, 9999))
            otp.save()

            email_body = 'Hi ' + user.full_name + \
                         ' Use the OTP below to verify your email \n' + str(otp.otp)
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            send_email.delay(data)

            return Response({'success': 'OTP sent successfully'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User with given email does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmailView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RequestPasswordResetEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.auth_provider != 'email':
                return Response({'error': 'Please continue your login using ' + user.auth_provider},
                                status=status.HTTP_400_BAD_REQUEST)

            if not user.is_verified:
                return Response({'error': 'Please verify your email first'}, status=status.HTTP_400_BAD_REQUEST)

            if hasattr(user, 'otp'):
                user.otp.delete()
                user.save()

            opt = OTP.objects.create(user=user, otp=random.randint(1000, 9999))
            opt.save()

            email_body = 'Hello, \nUse OTP below to reset your password\n' + str(opt.otp)
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your passsword'}

            send_email.delay(data)

            return Response({'success': 'We have sent you an OTP to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This email does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class CheckResetPasswordOTPView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmailVerficationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data['otp']
        try:
            main_otp = OTP.objects.get(otp=otp)
            user = main_otp.user

            time = user.otp.created_at + datetime.timedelta(minutes=1)
            current = timezone.now()
            if current > time:
                return Response({'error': 'OTP expired, request another one'}, status=status.HTTP_400_BAD_REQUEST)

            user.otp.delete()
            user.save()

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            return Response({'success': 'OTP verified successfully', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)

        except (ValueError, User.DoesNotExist, OTP.DoesNotExist):
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
