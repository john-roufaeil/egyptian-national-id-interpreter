# Generated by Django 5.1.5 on 2025-01-27 10:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0010_sessionapikey_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sessionapikey",
            name="key",
            field=models.CharField(max_length=32),
        ),
    ]
