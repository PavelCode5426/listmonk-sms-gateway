from rest_framework.views import APIView
from . import serializers
from config.injector import injector
from sms.services import WhatsAppServices, SMSServices


class SendMessageMixin(APIView):
    serializer_class = serializers.MessageSerializer
    service_class = None

    def get_service(self):
        return injector.get(self.service_class)


class WhatsAppSendMessages(SendMessageMixin):
    service_class = WhatsAppServices

    def create(self, request, *args, **kwargs):
        pass


class SMSSendMessages(SendMessageMixin):
    service_class = SMSServices

    def create(self, request, *args, **kwargs):
        pass
