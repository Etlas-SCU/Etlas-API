import environ
import numpy as np
from PIL import Image
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
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

    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_file = request.FILES['image']
        image = Image.open(image_file)
        image = np.array(image)
        detection = detect_monuments(image)
        return Response({'status': detection}, status=status.HTTP_200_OK)
