from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import messageSerializer
from .tasks import send_contact_us_email


class messageView(APIView):
    serializer_class = messageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email_body = f'full name: {serializer.data["full_name"]}\n email: {serializer.data["email"]}\n subject: {serializer.data["subject"]}\n message: {serializer.data["message"]}'
        data = {'email_body': email_body, 'email_subject': 'New message from contact us page'}

        send_contact_us_email.delay(data)

        return Response("Message sent successfully", status=status.HTTP_201_CREATED)
