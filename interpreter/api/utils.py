from .models import APICallLog

VALID_YEAR_RANGE = (1900, 2025)
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
    return (int(year) % 4 == 0 and int(year) % 100 != 0) or (int(year) % 400 == 0)


def log_api_call(national_id, api_key, endpoint, success):
    APICallLog.objects.create(
        national_id=national_id,
        api_key=api_key,
        endpoint=endpoint,
        success=success,
    )


def is_valid_national_id(national_id):
    # Check if first digit is valid (2 or 3)
    if national_id[0] not in ['2', '3']:
        return False

    century = "19" if national_id[0] == '2' else "20"
    year = century + national_id[1:3]
    month = national_id[3:5]
    day = national_id[5:7]
    governorate = national_id[7:9]
    gender = "female" if int(national_id[12]) % 2 == 0 else "male"
    serial_number = national_id[9:13]

    # Check if year is valid (between 1900 and 2025)
    if not (VALID_YEAR_RANGE[0] <= int(year) <= VALID_YEAR_RANGE[1]):
        return False

    # Check if month is valid (between 1 and 12)
    if int(month) > 12 or int(month) == 0:
        return False
    if int(month) == 2:
        valid_days = 29 if is_leap_year(year) else 28
    else:
        valid_days = 30 if int(month) in [4, 6, 9, 11] else 31

    # Check if day is valid (between 1 and 31)
    if int(day) > valid_days or int(day) == 0:
        return False

    # Check if governorate valid
    if governorate not in governorates:
        return False
    return True
