from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework_api_key.models import APIKey

from api.models import APICallLog
from .serializers import NationalIDSerializer, NationalIDDataSerializer, APIKeySerializer
from .utils import is_valid_national_id, log_api_call, governorates

API_KEY_HEADER = 'Api-Key '


class GenerateAPIKeyView(APIView):
    """
    Endpoint to generate an API Key for new sessions.
    """
    @extend_schema(responses=APIKeySerializer,)
    def get(self, request, *args, **kwargs):
        api_key, key = APIKey.objects.create_key(name="New Key")
        return Response({"api_key": key})


class NationalIDView(APIView):
    '''
    Endpoint to validate an Egyptian National ID number and extract information if valid.

    To retrieve your API Key, run the endpoint GET '/' to obtain the key. Once you have the key, use it in the request header as follows:
    "Api-Key <your-api-key>"
    '''
    @extend_schema(
        examples=[OpenApiExample("Example National ID", value={
                                 "national_id": "29001011234567"})],
        request=NationalIDSerializer,
        responses=NationalIDDataSerializer
    )
    def post(self, request, *args, **kwargs):
        api_key = request.META.get('HTTP_AUTHORIZATION', '').replace(
            API_KEY_HEADER, '').strip()
        endpoint = request.path
        if not api_key:
            return Response({"error": "API key is missing."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if not APIKey.objects.get_from_key(api_key):
                return Response({"error": "Invalid API key"}, status=status.HTTP_403_FORBIDDEN)
        except APIKey.DoesNotExist:
            return Response({"error": "Invalid API key"}, status=status.HTTP_403_FORBIDDEN)

        serializer = NationalIDSerializer(data=request.data)
        if serializer.is_valid():
            national_id = serializer.validated_data['national_id']

            # Check if length is 14 and only digits
            if len(national_id) != 14 or not national_id.isdigit():
                log_api_call(national_id, api_key, endpoint, False)
                return Response({"error": "National ID must be 14 digits."}, status=status.HTTP_400_BAD_REQUEST)

            if not is_valid_national_id(national_id):
                log_api_call(national_id, api_key, endpoint, False)
                return Response({"error": "National ID is invalid."}, status=status.HTTP_400_BAD_REQUEST)

            century = "19" if national_id[0] == '2' else "20"
            year = century + national_id[1:3]
            month = national_id[3:5]
            day = national_id[5:7]
            governorate = national_id[7:9]
            gender = "female" if int(national_id[12]) % 2 == 0 else "male"
            serial_number = national_id[9:13]
            log_api_call(national_id, api_key, endpoint, True)
            result = {
                "year": int(year),
                "month": month,
                "day": day,
                "governorate": governorates[governorate],
                "gender": {"ar": "أنثى" if gender == "female" else "ذكر", "en": gender},
                "serial_number": serial_number
            }
            return Response(result, status=status.HTTP_200_OK)

        log_api_call("None", api_key, endpoint, False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
