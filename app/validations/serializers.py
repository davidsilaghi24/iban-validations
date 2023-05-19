from rest_framework import serializers
from .models import IbanValidation
import re


def calculate_iban_checksum(iban):
    """
    Calculate the checksum of an IBAN.
    """
    iban = iban[4:] + iban[:4]
    iban = "".join(str(int(ch, 36)) if ch.isalpha() else ch for ch in iban)
    return int(iban) % 97 == 1


class IbanValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IbanValidation
        fields = ("iban", "valid", "timestamp")

    def validate_iban(self, value):
        """
        Validate the IBAN for Montenegro.
        """
        pattern = re.compile(r"^ME\d{2}\d{3}\d{13}\d{2}$")
        if not (bool(pattern.match(value)) and calculate_iban_checksum(value)):
            raise serializers.ValidationError("Invalid IBAN")

        country_code = value[:2]
        if country_code != "ME":
            raise serializers.ValidationError(
                "Invalid country code. Only Montenegro IBANs are allowed.")

        return value

    def create(self, validated_data):
        """
        Override the create method to calculate the IBAN validation status.
        """
        iban = validated_data.get('iban')
        pattern = re.compile(r"^ME\d{2}\d{3}\d{13}\d{2}$")
        valid = bool(pattern.match(iban) and calculate_iban_checksum(iban))

        # Remove 'valid' if it exists in validated_data
        validated_data.pop('valid', None)

        return IbanValidation.objects.create(valid=valid, **validated_data)
