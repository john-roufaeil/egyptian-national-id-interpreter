# Generated by Django 5.1.5 on 2025-01-27 09:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_sessionapikey_alter_apicalllog_api_key_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sessionapikey",
            name="api_key",
            field=models.CharField(
                default=django.utils.timezone.now, max_length=255, unique=True
            ),
            preserve_default=False,
        ),
    ]
