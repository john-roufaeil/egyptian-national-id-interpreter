from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view


@api_view(['POST'])
def index(request):
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

    try:
        # Check if 'national_id' exists in the request
        if 'national_id' not in request.data:
            return JsonResponse({"error": "Missing national_id in the request."}, status=400)

        national_id = request.data.get('national_id', '')

        if not isinstance(national_id, str):
            return JsonResponse({"error": "Input must be a string."}, status=400)

        # Check if length is 14 and only digits
        if len(national_id) != 14 or not national_id.isdigit():
            return JsonResponse({"error": "National ID must be 14 digits."}, status=400)

        century = "19" if national_id[0] == '2' else "20"
        year = century + national_id[1:3]
        month = national_id[3:5]
        day = national_id[5:7]
        governorate = national_id[7:9]
        gender = "female" if int(national_id[12]) % 2 == 0 else "male"
        serial_number = national_id[9:13]

        # Check if year is valid (between 1900 and 2025)
        if int(year) < 1900 or int(year) > 2025:
            return JsonResponse({"error": "National ID is invalid."}, status=400)

        # Check if month is valid (between 1 and 12)
        if int(month) > 12 or int(month) == 0:
            return JsonResponse({"error": "National ID is invalid."}, status=400)

        if month == 2:
            valid_days = 29 if is_leap_year(year) else 28
        elif month in [4, 6, 9, 11]:
            valid_days = 30
        else:
            valid_days = 31

        # Check if day is valid (between 1 and 31)
        if int(day) > valid_days or int(day) == 0:
            return JsonResponse({"error": "National ID is invalid."}, status=400)

        # Check if governorate valid
        if governorate not in governorates:
            return JsonResponse({"error": "National ID is invalid."}, status=400)

        result = {
            "year": int(year),
            "month": str(month).zfill(2),
            "day": str(day).zfill(2),
            "governorate": {
                "ar": governorates[governorate]["ar"],
                "en": governorates[governorate]["en"]
            },
            "gender": {
                "ar": "أنثى" if gender == "female" else "ذكر",
                "en": "female" if gender == "female" else "male"
            },
            "serial_number": serial_number
        }
        return JsonResponse({"res": result})

    except KeyError:
        return JsonResponse({"error": "Missing national_id in the request."}, status=400)
    except ValueError:
        return JsonResponse({"error": "Invalid value in the national_id."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
