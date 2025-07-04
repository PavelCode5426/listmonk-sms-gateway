from django.conf import settings
from injector import Module, Binder, singleton, provider

from sms.services import WhatsAppServices, SMSServices


class ServicesInjectorModule(Module):

    @singleton
    @provider
    def provide_whatspp_api_service(self) -> WhatsAppServices:
        host = settings.WHATSAPP_API_HOST
        username = settings.WHATSAPP_API_USERNAME
        password = settings.WHATSAPP_API_PASSWORD
        return WhatsAppServices(host, username, password)

    @singleton
    @provider
    def provide_sms_api_service(self) -> SMSServices:
        host = settings.SMS_API_HOST
        apikey = settings.SMS_API_TOKEN
        return SMSServices(host, apikey)

    def configure(self, binder: Binder) -> None:
        pass
