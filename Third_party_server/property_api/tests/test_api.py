from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from property_api.models import Property

class PropertyViewTests(APITestCase):
    
    def setUp(self):
        # Creating a sample property for testing
        self.property = Property.objects.create(
            cadastral_number="1234567890",
            latitude="50.4501",
            longitude="30.5234"
        )
        self.url = reverse('result')  

    def test_property_exists(self):
        """
        Test that the API returns True when the property exists
        """
        response = self.client.get(self.url, {'cadastral_number': self.property.cadastral_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], True)

    def test_property_does_not_exist(self):
        """
        Test that the API returns False when the property does not exist
        """
        response = self.client.get(self.url, {'cadastral_number': '0000000000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], False)

    def test_missing_cadastral_number(self):
        """
        Test that the API returns a 400 error when no cadastral number is provided
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Cadastral number is required")

    def test_invalid_cadastral_number(self):
        """
        Test that the API handles invalid cadastral numbers correctly
        """
        response = self.client.get(self.url, {'cadastral_number': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], False)
