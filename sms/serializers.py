from rest_framework import serializers

from . import models
from .models import Recipient, Campaign, Message, MessageRecipient


class RecipientSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = models.Recipient
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = models.Campaign
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    recipients = RecipientSerializer(many=True, write_only=True)
    campaign = CampaignSerializer(write_only=True)

    def create(self, validated_data):
        recipients = validated_data.pop('recipients')
        campaign = validated_data.pop('campaign')

        recipients_inserted = list()

        for recipient in recipients:
            recipients_inserted.append(
                Recipient.objects.update_or_create(uuid=recipient['uuid'], defaults=recipient,
                                                   create_defaults=recipient)[
                    0])

        campaign_inserted = \
            Campaign.objects.update_or_create(uuid=campaign['uuid'], defaults=campaign, create_defaults=campaign)[0]

        validated_data.update(campaign=campaign_inserted)
        message_inserted = Message.objects.create(**validated_data)

        MessageRecipient.objects.bulk_create(
            [MessageRecipient(recipient=recipient, message=message_inserted) for recipient in recipients_inserted])

        return message_inserted

    class Meta:
        model = models.Message
        exclude = ['using']


class WhatsAppMessageSerializer(MessageSerializer):
    def create(self, validated_data):
        validated_data.setdefault('using', 'whatsapp')
        return super().create(validated_data)


class SMSMessageSerializer(MessageSerializer):
    def create(self, validated_data):
        validated_data.setdefault('using', 'sms')
        return super().create(validated_data)
