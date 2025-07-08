import logging
import random
import time
from django.core.management.base import BaseCommand

from config.injector import injector
from sms.models import Message, MessageRecipient
from sms.services import WhatsAppServices, SMSServices


class Command(BaseCommand):
    help = 'Despacha los mensajes pendientes por enviar'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

        self.services = {
            'sms': injector.get(SMSServices),
            'whatsapp': injector.get(WhatsAppServices),
        }

    def handle(self, *args, **options):
        while True:
            messages = Message.objects.filter(recipients__success=False).all()

            service = self.services['sms']
            balance = service.getBalance()
            print(balance)

            for message in messages:
                self.stdout.write(f"Procesando: {message.subject} using {message.using}")
                try:
                    recipients = message.recipients.select_related('recipient').filter(success=False).all()
                    getattr(self, f'process_{message.using}')(message, recipients)
                except Exception as e:
                    logging.error(str(e))
            time.sleep(60)

    def process_sms(self, message, recipients):
        service = self.services['sms']
        for message_recipient in recipients:
            recipient = message_recipient.recipient
            cellnumber = recipient.attribs.get('phone')
            response = service.sendMessage(message.body, cellnumber)
            print(response)
            message_recipient.success = True
            message_recipient.save()

    def process_whatsapp(self, message, recipients):
        service = self.services['whatsapp']

        for message_recipient in recipients:
            recipient = message_recipient.recipient
            cellnumber = recipient.attribs.get('whatsapp')
            if cellnumber is None:
                logging.error(f"Recipients whatsapp are empty ID:{recipient.pk}")
                continue

            if cellnumber[0] == "+":
                cellnumber = cellnumber[1:]

            if not service.checkExists(cellnumber).json().get("numberExists"):
                continue

            response = service.startTyping(cellnumber)

            if response.status_code == 201:
                time.sleep(random.randint(5, 10))
                response = service.stopTyping(cellnumber)

            if response.status_code == 201:
                response = service.sendMessage(cellnumber, message.body)

            message_recipient.success = True
            message_recipient.save()
            time.sleep(random.randint(30, 60))
