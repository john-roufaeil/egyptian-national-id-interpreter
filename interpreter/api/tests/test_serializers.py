from rest_framework.test import APITestCase
from api.serializers import NationalIDDataSerializer, NationalIDSerializer, APIKeySerializer


class SerializersTest(APITestCase):
    def test_national_id_data_serializer_valid(self):
        data = {
            "year": 1990,
            "month": "01",
            "day": "15",
            "governorate": {"ar": "القاهرة", "en": "Cairo"},
            "gender": {"ar": "ذكر", "en": "male"},
            "serial_number": "1234"
        }
        serializer = NationalIDDataSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_national_id_data_serializer_invalid_year(self):
        data = {
            "year": "invalid",
            "month": "12",
            "day": "12",
            "governorate": {"ar": "القاهرة", "en": "Cairo"},
            "gender": {"ar": "ذكر"},
            "serial_number": "12"
        }
        serializer = NationalIDDataSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_national_id_serializer_valid(self):
        data = {"national_id": "29001011234567"}
        serializer = NationalIDSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_national_id_serializer_invalid(self):
        data = {"national_id": "invalid"}
        serializer = NationalIDSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_national_id_serializer_not_digits(self):
        data = {"national_id": "a" * 14}
        serializer = NationalIDSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_api_key_serializer_valid(self):
        data = {"api_key": "abcdefghijklmnopqrstuvwxyz123456"}
        serializer = APIKeySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_national_id_data_missing_field(self):
        data = {
            "year": 1990,
            "month": "01",
            "day": "15",
            "governorate": {"ar": "القاهرة", "en": "Cairo"},
            "serial_number": "1234"
            # Missing gender
        }
        serializer = NationalIDDataSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_national_id_serializer_missing_field(self):
        data = {}
        serializer = NationalIDSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_api_key_serializer_missing_field(self):
        data = {}
        serializer = APIKeySerializer(data=data)
        self.assertFalse(serializer.is_valid())
