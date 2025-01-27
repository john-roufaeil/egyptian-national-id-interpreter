from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework_api_key.models import APIKey
from .serializers import NationalIDSerializer
from .models import APICallLog, SessionAPIKey
from rest_framework_api_key.permissions import HasAPIKey


class GenerateAPIKeyView(APIView):
    def get(self, request, *args, **kwargs):
        api_key, key = APIKey.objects.create_key(name="New Key")
        return Response({"api_key": key})


class NationalIDView(APIView):
    """
    Endpoint to validate a National ID number and extract information from valid ones.
    """

    # permission_classes = [HasAPIKey]

    @extend_schema(request=NationalIDSerializer)
    def post(self, request, *args, **kwargs):
        api_key = request.headers.get(
            'Authorization', '').replace('Api-Key ', '').strip()
        endpoint = request.path
        if not api_key:
            return Response({"error": "API key is missing."}, status=400)
        try:
            if not APIKey.objects.get_from_key(api_key):
                return Response({"error": "Invalid API key"}, status=403)
        except APIKey.DoesNotExist:
            return Response({"error": "Invalid API key"}, status=403)

        governorates = {
            "01": {"ar": "القاهرة", "en": "Cairo"},
            "02": {"ar": "الإسكندرية", "en": "Alexandria"},
            "03": {"ar": "بورسعيد", "en": "Port Said"},
            "04": {"ar": "السويس", "en": "Suez"},
            "11": {"ar": "دمياط", "en": "Damietta"},
            "12": {"ar": "الدقهلية", "en": "Dakahlia"},
            "13": {"ar": "الشرقية", "en": "Sharqia"},
            "14": {"ar": "القليوبية", "en": "Qalyubia"},
            "15": {"ar": "كفر الشيخ", "en": "Kafr El Sheikh"},
            "16": {"ar": "الغربية", "en": "Gharbia"},
            "17": {"ar": "المنوفية", "en": "Menoufia"},
            "18": {"ar": "البحيرة", "en": "Beheira"},
            "19": {"ar": "الإسماعيلية", "en": "Ismailia"},
            "21": {"ar": "الجيزة", "en": "Giza"},
            "22": {"ar": "بني سويف", "en": "Beni Suef"},
            "23": {"ar": "الفيوم", "en": "Fayoum"},
            "24": {"ar": "المنيا", "en": "Minya"},
            "25": {"ar": "أسيوط", "en": "Assiut"},
            "26": {"ar": "سوهاج", "en": "Sohag"},
            "27": {"ar": "قنا", "en": "Qena"},
            "28": {"ar": "أسوان", "en": "Aswan"},
            "29": {"ar": "الأقصر", "en": "Luxor"},
            "31": {"ar": "البحر الأحمر", "en": "Red Sea"},
            "32": {"ar": "الوادي الجديد", "en": "New Valley"},
            "33": {"ar": "مطروح", "en": "Matrouh"},
            "34": {"ar": "شمال سيناء", "en": "North Sinai"},
            "35": {"ar": "جنوب سيناء", "en": "South Sinai"},
            "88": {"ar": "خارج الجمهورية", "en": "Outside Egypt"}
        }

        def is_leap_year(year):
            return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

        serializer = NationalIDSerializer(data=request.data)
        if serializer.is_valid():
            national_id = serializer.validated_data['national_id']

            APIKey.objects.filter(hashed_key=api_key).first()
            APICallLog.objects.create(
                national_id=national_id,
                api_key=api_key,
                endpoint=endpoint,
                success=True,
            )

            # Check if length is 14 and only digits
            if len(national_id) != 14 or not national_id.isdigit():
                return Response({"error": "National ID must be 14 digits."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if first digit is valid (2 or 3)
            if national_id[0] not in ['2', '3']:
                return Response({"error": "National ID is invalid."}, status=status.HTTP_400_BAD_REQUEST)

            century = "19" if national_id[0] == '2' else "20"
            year = century + national_id[1:3]
            month = national_id[3:5]
            day = national_id[5:7]
            governorate = national_id[7:9]
            gender = "female" if int(national_id[12]) % 2 == 0 else "male"
            serial_number = national_id[9:13]

            # Check if year is valid (between 1900 and 2025)
            if int(year) < 1900 or int(year) > 2025:
                return Response({"error": "National ID is invalid."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if month is valid (between 1 and 12)
            if int(month) > 12 or int(month) == 0:
                return Response({"error": "National ID is invalid."}, status=status.HTTP_400_BAD_REQUEST)

            if month == 2:
                valid_days = 29 if is_leap_year(year) else 28
            elif month in [4, 6, 9, 11]:
                valid_days = 30
            else:
                valid_days = 31

            # Check if day is valid (between 1 and 31)
            if int(day) > valid_days or int(day) == 0:
                return Response({"error": "National ID is invalid."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if governorate valid
            if governorate not in governorates:
                return Response({"error": "National ID is invalid."}, status=status.HTTP_400_BAD_REQUEST)

            result = {
                "year": int(year),
                "month": month,
                "day": day,
                "governorate": governorates[governorate],
                "gender": {"ar": "أنثى" if gender == "female" else "ذكر", "en": gender},
                "serial_number": serial_number
            }
            return Response(result, status=status.HTTP_200_OK)

        APICallLog.objects.create(
            national_id="None",
            api_key=api_key,
            endpoint=endpoint,
            success=False,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
