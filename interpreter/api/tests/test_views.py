from rest_framework.test import APITestCase
from rest_framework_api_key.models import APIKey
from rest_framework import status
from api.models import APICallLog
from api.utils import governorates
from api.serializers import NationalIDDataSerializer


class GenerateAPIKeyViewTests(APITestCase):
    def test_generate_api_key_success(self):
        """Test API key generation returns a 200 response with valid key."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("api_key", response.data)

    def test_generate_api_key_unique(self):
        """Ensure multiple API keys generated are unique."""
        response1 = self.client.get("/")
        response2 = self.client.get("/")
        self.assertNotEqual(
            response1.data['api_key'], response2.data['api_key'])


class NationalIDViewTests(APITestCase):
    def setUp(self):
        self.api_key, self.key = APIKey.objects.create_key(name="Test Key")
        self.headers = {"HTTP_AUTHORIZATION": f"Api-Key {self.key}"}

    # API Key Validation
    def test_missing_api_key(self):
        """Test request without API key returns 400."""
        response = self.client.post("/validate-national-id/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "API key is missing."})

    def test_invalid_api_key(self):
        """Test request with an invalid API key returns 403."""
        response = self.client.post(
            "/validate-national-id/",
            data={"national_id": "29001011234567"},
            HTTP_AUTHORIZATION="Api-Key invalid_key",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"error": "Invalid API key"})

    # Input Validation
    def test_empty_payload(self):
        """Test request with no payload returns 400."""
        response = self.client.post(
            "/validate-national-id/", {}, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_national_id(self):
        """Test a valid national ID returns correct data."""
        response = self.client.post(
            "/validate-national-id/",
            data={"national_id": "29001011234567"},
            **self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("year", response.data)
        self.assertIn("governorate", response.data)
        self.assertIn("gender", response.data)

    def test_invalid_national_id_logic(self):
        """Test an invalid national ID returns error."""
        response = self.client.post(
            "/validate-national-id/",
            data={"national_id": "12345678901234"},
            **self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "National ID is invalid."})

    # Governorate Validation
    def test_invalid_governorate(self):
        """Test invalid governorate code in national ID."""
        response = self.client.post(
            "/validate-national-id/",
            data={"national_id": "29001099345678"},
            **self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "National ID is invalid."})

    # Gender Validation
    def test_gender_female(self):
        """Test valid male national ID."""
        response = self.client.post(
            "/validate-national-id/",
            data={"national_id": "29001011234567"},
            **self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["gender"]["en"], "female")

    def test_gender_male(self):
        """Test valid female national ID."""
        response = self.client.post(
            "/validate-national-id/",
            data={"national_id": "29001011234518"},
            **self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["gender"]["en"], "male")

    # Leap Year Validation
    def test_non_leap_year(self):
        """Test invalid leap year national ID."""
        response = self.client.post(
            "/validate-national-id/",
            data={"national_id": "2000221234567"},
            **self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_leap_year(self):
        """Test valid date in leap year."""
        response = self.client.post(
            "/validate-national-id/",
            data={"national_id": "30002291234567"},
            **self.headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["day"], "29")

    # API Call Logging
    def test_successful_api_call_logging(self):
        """Test successful API calls are logged."""
        self.client.post(
            "/validate-national-id/",
            data={"national_id": "29001011234567"},
            **self.headers,
        )
        self.assertEqual(APICallLog.objects.count(), 1)
        log = APICallLog.objects.first()
        self.assertTrue(log.success)

    def test_failed_api_call_logging(self):
        """Test failed API calls are logged."""
        self.client.post(
            "/validate-national-id/",
            data={"national_id": "12345678901234"},
            **self.headers,
        )
        self.assertEqual(APICallLog.objects.count(), 1)
        log = APICallLog.objects.first()
        self.assertFalse(log.success)
