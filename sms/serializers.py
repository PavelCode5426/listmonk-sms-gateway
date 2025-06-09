from rest_framework import serializers


class RecipientAttribsSerializer(serializers.Serializer):
    phone = serializers.CharField()
    fcm_id = serializers.CharField()
    city = serializers.CharField()


class RecipientSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    email = serializers.EmailField()
    name = serializers.CharField()
    attribs = RecipientAttribsSerializer()
    status = serializers.CharField()


class CampaignSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    name = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())


class MessageSerializer(serializers.Serializer):
    subject = serializers.CharField()
    body = serializers.CharField()
    content_type = serializers.CharField()
    recipients = RecipientSerializer(many=True)
    campaign = CampaignSerializer()
