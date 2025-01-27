from django.db import models

class APICallLog(models.Model):
    api_key = models.CharField(max_length=255)
    national_id = models.CharField(max_length=255, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=255)
    success = models.BooleanField()

    def __str__(self):
        return f"{self.api_key[:8]} - {str(self.timestamp)[:19]} ({'Success' if self.success else 'Failed'}): {self.national_id}"
