from django.utils.deprecation import MiddlewareMixin
from .models import SessionAPIKey

class APIKeyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'api_key' not in request.session:
            api_key, key = SessionAPIKey.objects.create_key(name="Session Key")
            request.session['api_key'] = key
        request.api_key = request.session['api_key']
