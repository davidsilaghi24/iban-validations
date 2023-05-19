from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from validations.models import IbanValidation


class TestIbanViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.validate_iban_url = reverse('validations:validate-iban')
        cls.validation_history_url = reverse('validations:validation-history')
        cls.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_iban_validation_view_no_iban(self):
        response = self.client.post(self.validate_iban_url, data={'iban': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {'error': 'Invalid request. Please provide the IBAN.'})

    def test_iban_validation_view_with_iban_valid(self):
        response = self.client.post(self.validate_iban_url, data={
                                    'iban': 'ME25505000012345678951'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('valid', response.data)
        self.assertTrue(response.data['valid'])

    def test_iban_validation_view_with_iban_invalid_format(self):
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

        # Check that the response contains the 'history' key
        self.assertIn('history', response.data)

        # Check that the 'history' key contains the valid and invalid IBANs
        self.assertEqual(len(response.data['history']), 2)
        response_data = [item['iban'] for item in response.data['history']]
        self.assertIn(valid_iban.iban, response_data)
        self.assertIn(invalid_iban.iban, response_data)
