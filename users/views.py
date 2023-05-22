from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import IsTheCurrentUser
from .serializers import UserSerializer, BestScoreSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsTheCurrentUser]


class TotalBestScoreView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        total_best_score = user.best_score_monuments + user.best_Score_landmarks + user.best_score_statues

        return Response({'total_best_score': total_best_score}, status=status.HTTP_200_OK)

class BestScoreStatuesView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = BestScoreSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        best_score_statues = user.best_score_statues

        return Response({'best_score_statues': best_score_statues}, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=request.user.id)
        user.best_score_statues = max(user.best_score_statues, serializer.validated_data['new_score'])
        user.save()

        return Response({'best_score_statues': user.best_score_statues}, status=status.HTTP_200_OK)
    

class BestScoreLandmarksView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = BestScoreSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        best_score_landmarks = user.best_Score_landmarks

        return Response({'best_score_landmarks': best_score_landmarks}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=request.user.id)
        user.best_Score_landmarks = max(user.best_Score_landmarks, serializer.validated_data['new_score'])
        user.save()

        return Response({'best_score_landmarks': user.best_Score_landmarks}, status=status.HTTP_200_OK)
    
class BestScoreMonumentsView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = BestScoreSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        best_score_monuments = user.best_score_monuments

        return Response({'best_score_monuments': best_score_monuments}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=request.user.id)
        user.best_score_monuments = max(user.best_score_monuments, serializer.validated_data['new_score'])
        user.save()

        return Response({'best_score_monuments': user.best_score_monuments}, status=status.HTTP_200_OK)
