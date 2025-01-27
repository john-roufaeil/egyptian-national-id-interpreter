from rest_framework import serializers


class NationalIDDataSerializer(serializers.Serializer):
    """
    Serializer for parsing and validating National ID data.
    """

    year = serializers.IntegerField()
    month = serializers.CharField(max_length=2)
    day = serializers.CharField(max_length=2)
    governorate = serializers.DictField(child=serializers.CharField())
    gender = serializers.DictField(child=serializers.CharField())
    serial_number = serializers.CharField(max_length=4)


class NationalIDSerializer(serializers.Serializer):
    """
    Serializer for validating a National ID number.
    """

    national_id = serializers.RegexField(
        regex=r"^\d{14}$",
        max_length=14,
        min_length=14,
        help_text="The national ID number.",
    )


class APIKeySerializer(serializers.Serializer):
    """
    Serializer for api key.
    """

    api_key = serializers.CharField(max_length=64, help_text="The API Key.")
