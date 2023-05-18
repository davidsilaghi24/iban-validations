from rest_framework import status, generics
from rest_framework.response import Response
from .models import IbanValidation
from .serializers import IbanValidationSerializer
import re


class IbanValidationView(generics.CreateAPIView):
    queryset = IbanValidation.objects.all()
    serializer_class = IbanValidationSerializer

    def create(self, request, *args, **kwargs):
        # Check if iban is provided
        iban = request.data.get('iban', None)
        if not iban:
            return Response({"error": "Invalid request. Please check the entered IBAN."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Perform the IBAN validation here
        pattern = re.compile(r"^ME\d{2}\d{3}\d{13}\d{2}$")
        valid = pattern.match(iban) is not None

        # Create the IbanValidation instance with the validated data and the validation result
        IbanValidation.objects.create(iban=iban, valid=valid)

        # Return 200 OK as per the requirement, whether the IBAN is valid or not
        return Response({"iban": iban, "valid": valid}, status=status.HTTP_200_OK)


class IbanValidationHistoryView(generics.ListAPIView):
    queryset = IbanValidation.objects.all()
    serializer_class = IbanValidationSerializer
