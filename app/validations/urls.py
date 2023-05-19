from django.urls import path
from .views import (
    IbanValidationView,
    IbanValidationHistoryView,
    IbanInfoView
)

app_name = 'validations'

urlpatterns = [
    path('validate-iban', IbanValidationView.as_view(), name='validate-iban'),
    path('validation-history', IbanValidationHistoryView.as_view(),
         name='validation-history'),
    path('iban-info/', IbanInfoView.as_view(), name='iban-info'),
]
