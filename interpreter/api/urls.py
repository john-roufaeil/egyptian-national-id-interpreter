from django.urls import path
from .views import NationalIDView, GenerateAPIKeyView

urlpatterns = [
    path('validate-national-id/', NationalIDView.as_view(),
         name='validate-national-id'),
    path('', GenerateAPIKeyView.as_view(), name='generate-api-key'),

]
