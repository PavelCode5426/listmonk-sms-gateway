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
    tags = models.JSONField(default=list)


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    using = models.CharField(max_length=255, choices=[('SMS', 'sms'), ('WhatsApp', 'whatsapp')])
    content_type = models.CharField(max_length=255)
    recipients = models.ManyToManyField(Recipient)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

