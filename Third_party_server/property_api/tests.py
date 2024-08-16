from unittest import mock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from property_api.models import Property

class PropertyViewTests(APITestCase):

    def setUp(self):
        # Creating a sample property to test with a valid cadastral number
        self.valid_property = Property.objects.create(
            cadastral_number='1234567890',
            latitude=45.0,
            longitude=90.0,
        )
        self.valid_cadastral_number = '1234567890'
        self.invalid_cadastral_number = ''
        self.url = reverse('result')  # Use the appropriate URL name

    def test_valid_cadastral_number(self):
        """
        Ensure that providing a valid cadastral number returns the correct property data.
        """
        response = self.client.get(self.url, {'cadastral_number': self.valid_cadastral_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cadastral_number'], self.valid_cadastral_number)

    def test_cadastral_number_not_in_db(self):
        """
        Ensure that providing a cadastral number that doesn't exist in the DB returns 404 error.
        """
        response = self.client.get(self.url, {'cadastral_number': "123"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    
    def test_invalid_cadastral_number(self):
        """
        Ensure that providing an invalid cadastral number returns a 400 response.
        """
        response = self.client.get(self.url, {'cadastral_number': self.invalid_cadastral_number})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_cadastral_number(self):
        """
        Ensure that not providing a cadastral number returns a 400 response.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Cadastral number is required')

    def test_unexpected_error(self):
        """
        Simulate an unexpected error by mocking the Property.objects.get method.
        """
        with mock.patch('property_api.models.Property.objects.get') as mock_get:
            mock_get.side_effect = Exception("Unexpected error")
            response = self.client.get(self.url, {'cadastral_number': self.valid_cadastral_number})
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn('error', response.data)

