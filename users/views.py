from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User
from .permissions import IsTheCurrentUser
from .serializers import UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsTheCurrentUser]
