from rest_framework import viewsets, status
from users.models import User
from .serializers import RegisterSerializer
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from .tasks import verification_mail
import uuid
import environ

env = environ.Env()

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
        token = user.email_verification_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email_verify')
        absurl = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = 'Hi '+ user.full_name + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        verification_mail.delay(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmailView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def retrieve(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            user = User.objects.get(email_verification_token=uuid.UUID(token))
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return redirect(f"{env('WEB_ROOT_URL')}/signin")
        except (ValueError, User.DoesNotExist):
            return redirect(f"{env('WEB_ROOT_URL')}/invalid_token")
