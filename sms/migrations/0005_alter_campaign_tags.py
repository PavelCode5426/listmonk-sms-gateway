# Generated by Django 5.2.4 on 2025-07-06 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0004_alter_messagerecipient_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='tags',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
