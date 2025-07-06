from rest_framework import status
from rest_framework.generics import CreateAPIView
from . import models
from .serializers import WhatsAppMessageSerializer, SMSMessageSerializer
from rest_framework.response import Response


class SendMessageMixin(CreateAPIView):
    queryset = models.Message.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class WhatsAppSendMessages(SendMessageMixin):
    serializer_class = WhatsAppMessageSerializer


class SMSSendMessages(SendMessageMixin):
    serializer_class = SMSMessageSerializer
