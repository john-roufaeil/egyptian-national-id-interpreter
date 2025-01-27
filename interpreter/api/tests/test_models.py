import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import APICallLog


class APICallLogTest(TestCase):
    def setUp(self):
        self.log = APICallLog.objects.create(
            api_key='test_api_key',
            national_id='1234567890',
            endpoint='/api/v1/data',
            success=False,
        )

    def test_model_creation(self):
        self.assertEqual(self.log.api_key, 'test_api_key')
        self.assertEqual(self.log.national_id, '1234567890')
        self.assertEqual(self.log.endpoint, '/api/v1/data')
        self.assertFalse(self.log.success)

    def test_api_key_max_length(self):
        with self.assertRaises(ValidationError):
            APICallLog.objects.create(
                api_key='x' * 65,
                national_id='1234567890',
                endpoint='/api/v1/data',
                success=False,
            )

    def test_national_id_max_length(self):
        with self.assertRaises(ValidationError):
            APICallLog.objects.create(
                api_key='test_api_key',
                national_id='x' * 15,
                endpoint='/api/v1/data',
                success=False,
            )

    def test_endpoint_max_length(self):
        with self.assertRaises(ValidationError):
            APICallLog.objects.create(
                api_key='test_api_key',
                national_id='1234567890',
                endpoint='x' * 51,
                success=False,
            )

    def test_timestamp_auto_now_add(self):
        self.assertIsNotNone(self.log.timestamp)

    def test_success_field_boolean(self):
        self.assertFalse(self.log.success)

    def test_missing_api_key(self):
        with self.assertRaises(ValidationError):
            log = APICallLog(endpoint='/api/v1/data',
                             national_id='1234567890', success=False)
            log.full_clean()

    def test_missing_endpoint(self):
        with self.assertRaises(ValidationError):
            log = APICallLog(api_key='test_api_key',
                             national_id='1234567890', success=False)
            log.full_clean()

    def test_missing_success(self):
        with self.assertRaises(ValidationError):
            log = APICallLog(api_key='test_api_key',
                             national_id='1234567890', endpoint='/api/v1/data')
            log.full_clean()

    def test_empty_api_key(self):
        with self.assertRaises(ValidationError):
            log = APICallLog(api_key='', national_id='1234567890',
                             endpoint='/api/v1/data', success=False)
            log.full_clean()

    def test_empty_endpoint(self):
        with self.assertRaises(ValidationError):
            log = APICallLog(api_key='test_api_key',
                             national_id='1234567890', endpoint='', success=False)
            log.full_clean()

    def test_special_characters_in_endpoint(self):
        log = APICallLog.objects.create(
            api_key='test_api_key',
            national_id='1234567890',
            endpoint='/api/v1/data?param=value#section',
            success=True,
        )
        log.full_clean()
        self.assertIn('?', log.endpoint)
        self.assertIn('#', log.endpoint)

    def test_duplicate_national_id(self):
        APICallLog.objects.create(
            api_key='another_api_key',
            national_id='1234567890',
            endpoint='/api/v1/another_data',
            success=True,
        )
        self.assertEqual(APICallLog.objects.filter(
            national_id='1234567890').count(), 2)

    def test_str_representation_success(self):
        self.log.success = True
        self.log.save()
        expected_str = f"{self.log.api_key[:8]} - {str(self.log.timestamp)[:19]} (Success): {self.log.national_id}"
        self.assertEqual(str(self.log), expected_str)

    def test_str_representation_failure(self):
        expected_str = f"{self.log.api_key[:8]} - {str(self.log.timestamp)[:19]} (Failed): {self.log.national_id}"
        self.assertEqual(str(self.log), expected_str)

    def test_filter_by_success(self):
        successful_log = APICallLog.objects.create(
            api_key='successful_api_key',
            national_id='9876543210',
            endpoint='/api/v1/success_data',
            success=True,
        )
        failed_logs = APICallLog.objects.filter(success=False)
        successful_logs = APICallLog.objects.filter(success=True)
        self.assertEqual(failed_logs.count(), 1)
        self.assertEqual(successful_logs.count(), 1)
        self.assertIn(successful_log, successful_logs)

    def test_delete_log(self):
        self.log.delete()
        self.assertEqual(APICallLog.objects.filter(
            api_key='test_api_key').count(), 0)

    def test_update_log(self):
        self.log.success = True
        self.log.save()
        self.assertTrue(APICallLog.objects.get(id=self.log.id).success)

    def test_bulk_create_logs(self):
        logs = [
            APICallLog(
                api_key=f'api_key_{i}',
                national_id=f'123456789{i}',
                endpoint=f'/api/v1/endpoint_{i}',
                success=bool(i % 2),
            )
            for i in range(10)
        ]
        APICallLog.objects.bulk_create(logs)
        self.assertEqual(APICallLog.objects.count(), 11)

    def test_invalid_data_type_for_success(self):
        with self.assertRaises(ValidationError):
            log = APICallLog(
                api_key='test_api_key',
                national_id='1234567890',
                endpoint='/api/v1/data',
                success='not_a_boolean',
            )
            log.full_clean()
