from django.test import TestCase
from api.utils import is_valid_national_id, is_leap_year, governorates


class UtilsTest(TestCase):

    def test_is_leap_year_true(self):
        self.assertTrue(is_leap_year(2000))
        self.assertTrue(is_leap_year(2024))

    def test_is_leap_year_false(self):
        self.assertFalse(is_leap_year(1900))
        self.assertFalse(is_leap_year(2023))

    def test_is_valid_national_id_valid(self):
        self.assertTrue(is_valid_national_id("29001011234567"))  # Valid ID

    def test_is_valid_national_id_invalid_century(self):
        self.assertFalse(is_valid_national_id(
            "49001011234567"))  # Invalid first digit

    def test_is_valid_national_id_invalid_month(self):
        self.assertFalse(is_valid_national_id(
            "29013311234567"))  # Invalid month

    def test_is_valid_national_id_invalid_day(self):
        self.assertFalse(is_valid_national_id("29001332234567"))  # Invalid day

    def test_is_valid_national_id_invalid_governorate(self):
        self.assertFalse(is_valid_national_id(
            "29011069234567"))  # Invalid governorate

    def test_is_valid_national_id_invalid_format(self):
        self.assertFalse(is_valid_national_id(
            "ABC01011234567"))  # Contains letters

    def test_governorates_key_exists(self):
        self.assertIn("01", governorates)
        self.assertEqual(governorates["01"]["en"], "Cairo")
