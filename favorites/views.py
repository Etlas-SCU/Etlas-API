from django.http import Http404
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favorite
from .serializers import FavoriteSerializer, FavoriteCreateDestroySerializer


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


class FavoriteMonumentDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteCreateDestroySerializer
    lookup_field = None
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj_id = serializer.validated_data['id']
            instance = get_object_or_404(Favorite, user=self.request.user, monument=obj_id)
            self.perform_destroy(instance)
            return Response({"message": "The Monument has been deleted from your favorites."}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'detail': 'Monument not found.'}, status=status.HTTP_404_NOT_FOUND)


class FavoriteArticleDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteCreateDestroySerializer
    lookup_field = None
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj_id = serializer.validated_data['id']
            instance = get_object_or_404(Favorite, user=self.request.user, article=obj_id)
            self.perform_destroy(instance)
            return Response({"message": "The Article has been deleted from your favorites."},
                            status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'detail': 'Article not found.'}, status=status.HTTP_404_NOT_FOUND)
