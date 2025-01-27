from django.conf import settings

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object


class ApiKeyScheme(OpenApiAuthenticationExtension):
    target_class = 'rest_framework.authentication.ApiAuthentication'
    name = 'cookieAuth'
    priority = -1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': settings.SESSION_COOKIE_NAME,
        }
