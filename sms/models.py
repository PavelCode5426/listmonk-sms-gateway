from django.db import models


class Recipient(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    email = models.EmailField()
    name = models.CharField(max_length=255)
    attribs = models.JSONField(default=dict)
    status = models.CharField(max_length=255)


class Campaign(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    tags = models.JSONField(default=list, blank=True,null=True)


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    using = models.CharField(max_length=255, choices=[('SMS', 'sms'), ('WhatsApp', 'whatsapp')])
    content_type = models.CharField(max_length=255)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MessageRecipient(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='messages')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='recipients')
    success = models.BooleanField(default=False)
