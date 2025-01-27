from django.core.exceptions import ValidationError
from django.db import models


class APICallLog(models.Model):
    api_key = models.CharField(max_length=64)
    national_id = models.CharField(max_length=14, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=50)
    success = models.BooleanField()

    def __str__(self):
        return (
            f"{self.api_key[:8]} - {str(self.timestamp)[:19]}"
            f"({'Success' if self.success else 'Failed'}): {self.national_id}"
        )

    def clean(self):
        if len(self.api_key) > 64:
            raise ValidationError(
                {"api_key": "API Key exceeds maximum length of 32 characters."}
            )
        if len(self.national_id) > 14:
            raise ValidationError(
                {"national_id": "National ID exceeds maximum length of 14 characters."}
            )
        if len(self.endpoint) > 50:
            raise ValidationError(
                {"endpoint": "Endpoint URL exceeds maximum length of 50 characters."}
            )
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
