from django.urls import path

from . import views

app_name = "sms"
urlpatterns = [
    path(r'whatsapp', views.WhatsAppSendMessages.as_view(), name='whatsapp'),
    path(r'sms', views.SMSSendMessages.as_view(), name='sms'),
]
