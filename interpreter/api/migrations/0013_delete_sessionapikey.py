# Generated by Django 5.1.5 on 2025-01-27 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_sessionapikey_key'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SessionAPIKey',
        ),
    ]
