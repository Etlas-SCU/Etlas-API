from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializer
from .tasks import send_contact_us_email


class MessageView(GenericAPIView):
    serializer_class = MessageSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email_body = f'full name: {serializer.validated_data["full_name"]}\nemail: {serializer.validated_data["email"]}\nsubject: {serializer.validated_data["subject"]}\nmessage: {serializer.validated_data["message"]}'
        data = {'email_body': email_body, 'email_subject': 'New message from contact us page'}

        send_contact_us_email.delay(data)

        return Response({"success": "Message sent successfully"}, status=status.HTTP_201_CREATED)
