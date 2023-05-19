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
        fields = ("iban", "valid")

    def validate_iban(self, value):
        """
        Validate the IBAN.
        """
        pattern = re.compile(r"^ME\d{2}\d{3}\d{13}\d{2}$")
        self.valid = bool(pattern.match(
            value) and calculate_iban_checksum(value))
        return value

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["valid"] = getattr(
            self, "valid", None
        )  # Use stored result, default to None
        return ret
