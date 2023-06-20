from rest_framework import status, viewsets
from rest_framework.response import Response

from users.models import User
from .serializers import (FacebookSocialAuthSerializer,
                          GoogleSocialAuthSerializer, TwitterAuthSerializer)


# Create your views here.


class GoogleSocialAuthView(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = GoogleSocialAuthSerializer

    def create(self, request, *args, **kwargs):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data))
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = FacebookSocialAuthSerializer

    def create(self, request, *args, **kwargs):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class TwitterSocialAuthView(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = TwitterAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
