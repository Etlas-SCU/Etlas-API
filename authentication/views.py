from rest_framework import viewsets, status, views, generics
from users.models import User
from .serializers import RegisterSerializer, EmailVerficationSerializer, LoginSerializer, RequestPasswordResetEmailSerializer, SetNewPasswordSerializer, LogoutSerializer
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from .tasks import send_email
import uuid
import environ
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponsePermanentRedirect

env = environ.Env()

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [env('APP_SCHEME'), 'http', 'https']

# Create your views here.

class RegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        user_data = serializer.data

        redirect_url = request.data.get('redirect_url', '')

        user = User.objects.get(email=user_data['email'])
        token = user.email_verification_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email_verify')
        absurl = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = 'Hi '+ user.full_name + \
            ' Use the link below to verify your email \n' + absurl + "&redirect_url=" + redirect_url
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        send_email.delay(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmailView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmailVerficationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])

    def retrieve(self, request, *args, **kwargs):
        token = request.GET.get('token')
        redirect_url = request.GET.get('redirect_url', '')
        print(token)
        try:
            user = User.objects.get(email_verification_token=uuid.UUID(token))
            if not user.is_verified:
                user.is_verified = True
                user.save()

            if len(redirect_url) > 3:
                return CustomRedirect(f"{redirect_url}?email=Successfully activated")
            else:
                return CustomRedirect(f"{env('WEB_ROOT_URL')}/signin?email=Successfully activated")
            
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            
        except (ValueError, User.DoesNotExist):
            if len(redirect_url) > 3:
                return CustomRedirect(f"{redirect_url}?token=Invalid token")
            else:
                return CustomRedirect(f"{env('WEB_ROOT_URL')}/invalid_token")

            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


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
        
        email = request.data.get('email', '')
        redirect_url = request.data.get('redirect_url', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.auth_provider == "email":
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                
                current_site = get_current_site(request=request).domain
                relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
                absurl = 'http://'+current_site + relativeLink
                email_body = 'Hello, \nUse link below to reset your password\n' + absurl + "?redirect_url=" + redirect_url
                data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your passsword'}
                
                send_email.delay(data)
                return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Please continue your login using ' + user.auth_provider}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'error': 'This email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordTokenCheckView(views.APIView):
    
    def get(self, request, uidb64, token):
        try:
            redirect_url = request.GET.get('redirect_url', '')
            print(redirect_url)
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(f"{redirect_url}?token_valid=False")
                else:
                    return CustomRedirect(f"{env('WEB_ROOT_URL')}/invalid_token?token_valid=False")

                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if len(redirect_url) > 3:
                return CustomRedirect(f"{redirect_url}?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}")
            else:
                return CustomRedirect(f"{env('WEB_ROOT_URL')}/reset_password?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}")
            
            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
        
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
