from django.contrib import admin
from .models import SessionAPIKey, APICallLog

admin.site.register(SessionAPIKey)
admin.site.register(APICallLog)
