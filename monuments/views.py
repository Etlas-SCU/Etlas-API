import environ
import numpy as np
from PIL import Image
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from roboflow import Roboflow

from monuments.models import Monument
from monuments.serializers import MonumentSerializer, ImageSerializer

env = environ.Env()

rf = Roboflow(api_key=env('ROBOFLOW_API_KEY'))
project = rf.workspace().project("monuments-detection")
model = project.version(3).model


def detect_monuments(image):
    prediction = model.predict(image, confidence=70, overlap=25).json()['predictions']
    if not len(prediction):
        return "No monuments detected"
    else:
        return prediction[0]['class']


class MonumentListView(generics.ListAPIView):
    """ List all Monuments """
    queryset = Monument.objects.all()
    serializer_class = MonumentSerializer


class MonumentDetailView(generics.RetrieveAPIView):
    """ Retrieve a single Monument """
    queryset = Monument.objects.all()
    serializer_class = MonumentSerializer


class MonumentDetectionView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.scans_left <= 0:
            return Response({'status': 'You have no scans left'}, status=status.HTTP_403_FORBIDDEN)
        request.user.scans_left -= 1
        request.user.save()
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_file = request.FILES['image']
        image = Image.open(image_file)
        image = np.array(image)
        detection = detect_monuments(image)

        if detection == "No monuments detected":
            return Response({'Detection': detection}, status=status.HTTP_404_NOT_FOUND)
        
        monument = Monument.objects.filter(name__icontains=detection).first()

        return Response({'Detection': detection, 'Monument': MonumentSerializer(monument).data}, status=status.HTTP_200_OK)
