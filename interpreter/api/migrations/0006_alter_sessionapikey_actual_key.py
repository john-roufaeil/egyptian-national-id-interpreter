# Generated by Django 5.1.5 on 2025-01-27 09:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_remove_sessionapikey_api_key_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sessionapikey",
            name="actual_key",
            field=models.CharField(max_length=255),
        ),
    ]
