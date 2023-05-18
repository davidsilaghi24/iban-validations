from rest_framework import serializers
from .models import IbanValidation


class IbanValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IbanValidation
        fields = '__all__'

    def to_representation(self, instance):
        """
        Override the `to_representation` method to change the representation
        of `valid` field in the serialized data.

        In our case, we want the `valid` field to be represented as it is
        (True or False) in the serialized data. By default, Django Rest Framework
        serializes BooleanFields as `true` or `false` (lower case). However, we want
        the boolean representation to be `True` or `False` (Title case) in the
        serialized data.

        This method is called when converting the model instance into
        a native Python datatype, ready for outputting as a response.

        Args:
            instance: The model instance that is being serialized.

        Returns:
            A dictionary-like object representing the serialized data of the model instance.
        """
        ret = super().to_representation(instance)
        ret['valid'] = instance.valid
        return ret
