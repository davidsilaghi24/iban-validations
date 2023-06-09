from .validation_helpers import extract_iban_details
from .models import IbanValidation
from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import IbanValidationSerializer, IbanInfoSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "username": user.username}
        )


class IbanValidationView(generics.CreateAPIView):
    queryset = IbanValidation.objects.all()
    serializer_class = IbanValidationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.initial_data.get("iban"):
            return Response(
                {"error": "Invalid request. Please provide the IBAN."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response_data = serializer.data.copy()
            # remove the 'timestamp' field
            response_data.pop('timestamp', None)

            return Response(response_data, status=status.HTTP_200_OK)
        except serializers.ValidationError:
            return Response({"valid": False}, status=status.HTTP_200_OK)


class IbanValidationHistoryView(generics.ListAPIView):
    queryset = IbanValidation.objects.all().order_by("-timestamp")
    serializer_class = IbanValidationSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"history": serializer.data})


class IbanInfoView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IbanInfoSerializer

    def post(self, request, format=None):
        iban = request.data.get("iban")
        if iban:
            info = extract_iban_details(iban)
            return Response(info)
        else:
            return Response(
                {"error": "No IBAN provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
