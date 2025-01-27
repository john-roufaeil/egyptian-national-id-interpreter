from django.db import models
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey, AbstractAPIKey  # type: ignore
from django.utils.crypto import get_random_string
from django.utils.timezone import now


class SessionAPIKey(AbstractAPIKey):
    @classmethod
    def create_key(cls, name):
        key = get_random_string(32)
        # Add 'created' explicitly
        session_api_key = cls(name=name, created=now())
        session_api_key.save()
        return session_api_key, key

    def __str__(self):
        return f"{self.name} - {self.prefix}"


class APICallLog(models.Model):
    api_key = models.CharField(max_length=255)
    national_id = models.CharField(max_length=255, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=255)
    success = models.BooleanField()

    def __str__(self):
        return self.api_key + '-' + self.timestamp + " (" + self.success + ")"
