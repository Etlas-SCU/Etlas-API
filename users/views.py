from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, BestScoreSerializer, ImageUpdateSerializer, ChangePasswordSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class ChangeImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = ImageUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = self.serializer_class(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.validated_data['new_password'] != serializer.validated_data['confirm_new_password']:
            return Response({'confirm_new_password': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'success': 'Password changed successfully.'}, status=status.HTTP_200_OK)
