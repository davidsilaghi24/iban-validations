from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from validations.models import IbanValidation


class TestIbanViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.validate_iban_url = reverse('validations:validate-iban')
        cls.validation_history_url = reverse('validations:validation-history')

    def test_iban_validation_view_no_iban(self):
        response = self.client.post(self.validate_iban_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_iban_validation_view_with_iban_valid(self):
        response = self.client.post(
            self.validate_iban_url, data={'iban': 'ME25505000012345678951'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('valid', response.data)
        self.assertTrue(response.data['valid'])

    def test_iban_validation_view_with_iban_invalid(self):
        response = self.client.post(
            self.validate_iban_url, data={'iban': 'INVALID'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('valid', response.data)
        self.assertFalse(response.data['valid'])

    def test_iban_validation_history_view(self):
        # Create a valid IBAN record
        valid_iban = IbanValidation.objects.create(
            iban="ME25505000012345678951", valid=True)
        # Create an invalid IBAN record
        invalid_iban = IbanValidation.objects.create(
            iban="INVALID", valid=False)

        response = self.client.get(self.validation_history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the valid and invalid IBANs
        self.assertEqual(len(response.data), 2)
        response_data = {item['iban']: item['valid'] for item in response.data}
        self.assertTrue(response_data[valid_iban.iban])
        self.assertFalse(response_data[invalid_iban.iban])
