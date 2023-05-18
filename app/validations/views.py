from rest_framework import status, generics
from rest_framework.response import Response
from .models import IbanValidation
from .serializers import IbanValidationSerializer
import re


class IbanValidationView(generics.CreateAPIView):
    queryset = IbanValidation.objects.all()
    serializer_class = IbanValidationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Perform the IBAN validation here
        iban = serializer.validated_data['iban']
        pattern = re.compile(r"^ME\d{2}\d{3}\d{13}\d{2}$")
        valid = pattern.match(iban) is not None

        # Create the IbanValidation instance with the validated data and the validation result
        IbanValidation.objects.create(iban=iban, valid=valid)

        # Return 200 OK as per the requirement, whether the IBAN is valid or not
        return Response({"valid": valid}, status=status.HTTP_200_OK)


class IbanValidationHistoryView(generics.ListAPIView):
    queryset = IbanValidation.objects.all()
    serializer_class = IbanValidationSerializer
