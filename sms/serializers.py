from rest_framework import serializers

from . import models
from .models import Recipient, Campaign, Message


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
    recipients = RecipientSerializer(many=True)
    campaign = CampaignSerializer()

    class Meta:
        model = models.Message
        exclude = ['using']


class WhatsAppMessageSerializer(MessageSerializer):
    def create(self, validated_data):
        validated_data.setdefault('using', 'whatsapp')
        recipients = validated_data.pop('recipients')
        campaign = validated_data.pop('campaign')

        recipients_inserted = [Recipient.objects.update_or_create(defaults=recipient, create_defaults=recipient)[0] for
                               recipient in recipients]
        campaign_inserted = Campaign.objects.update_or_create(defaults=campaign, create_defaults=campaign)[0]

        message_inserted = Message.objects.create(**validated_data, campaign=campaign_inserted)
        message_inserted.recipients.add(*recipients_inserted)

        return message_inserted
