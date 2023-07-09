from django.http import Http404
from rest_framework import generics, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favorite
from .serializers import FavoriteSerializer, FavoriteCreateDestroySerializer, IsFavoriteSerializer


class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteDetailView(generics.RetrieveAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteMonumentCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteCreateDestroySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        favorite = Favorite.objects.filter(user=self.request.user, monument_id=serializer.validated_data['id'])
        if favorite.exists():
            return Response({"message": "This Monument is Already in Your Favorites."},
                            status=status.HTTP_400_BAD_REQUEST)
        favorite = Favorite.objects.create(user=self.request.user, monument_id=serializer.validated_data['id'])
        return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)


class FavoriteArticleCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteCreateDestroySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        favorite = Favorite.objects.filter(user=self.request.user, article_id=serializer.validated_data['id'])
        if favorite.exists():
            return Response({"message": "This Article is Already in Your Favorites."},
                            status=status.HTTP_400_BAD_REQUEST)
        favorite = Favorite.objects.create(user=self.request.user, article_id=serializer.validated_data['id'])
        return Response(FavoriteSerializer(favorite).data, status=status.HTTP_201_CREATED)


class FavoriteMonumentDeleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, *args, **kwargs):
        user = self.request.user
        try:
            instance = Favorite.objects.get(user=user, monument_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({"message": "The Monument is not in your favorites."}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteArticleDeleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, *args, **kwargs):
        user = self.request.user
        try:
            instance = Favorite.objects.get(user=user, article_id=id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({"message": "The Article is not in your favorites."}, status=status.HTTP_400_BAD_REQUEST)


class IsFavoriteView(views.APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"is_favorite": False}, status=status.HTTP_200_OK)
        serializer = IsFavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        favorite = None
        if data.get('monument_id'):
            favorite = Favorite.objects.filter(user=self.request.user, monument_id=data.get('monument_id'))
        elif data.get('article_id'):
            favorite = Favorite.objects.filter(user=self.request.user, article_id=data.get('article_id'))

        if favorite is None:
            return Response({"is_favorite": False}, status=status.HTTP_200_OK)
        return Response({"is_favorite": favorite.exists()}, status=status.HTTP_200_OK)
