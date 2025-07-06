from rest_framework.generics import CreateAPIView
from . import serializers, models
from .serializers import WhatsAppMessageSerializer, SMSMessageSerializer


class SendMessageMixin(CreateAPIView):
    queryset = models.Message.objects.all()


class WhatsAppSendMessages(SendMessageMixin):
    serializer_class = WhatsAppMessageSerializer


class SMSSendMessages(SendMessageMixin):
    serializer_class = SMSMessageSerializer
