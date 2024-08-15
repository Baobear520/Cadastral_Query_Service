from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from query_api.models import Query
from query_api.serializers import QuerySerializer


class QueryAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('query-list')
        
    @patch('query_api.tasks.send_query.delay')
    def test_create_query(self, mock_send_query_delay):
        """
        Test creating a new query via the /query endpoint
        """
        # Initial dummy data for testing
        data = {
            'cadastral_number': '555',
            'latitude': 50.4502,
            'longitude': 30.5231
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('query_id', response.data)
        self.assertEqual(Query.objects.count(), 1)
        self.assertEqual(Query.objects.get().cadastral_number, '555')
        # Assert that the Celery task was called
        mock_send_query_delay.assert_called_once_with(Query.objects.first().id)
    
    def test_create_query_invalid_cadastral_num(self):
        """
        Test creating a new query with invalid cadastral number
        """
        invalid_payload = {
            'cadastral_number': '',
            'latitude': 50.4501,
            'longitude': 30.5234,
        }
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_latitude_above_max_value(self):
        data = {
            "cadastral_number": "123456",
            "latitude": 91.0,  # Invalid latitude (greater than 90)
            "longitude": 45.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('latitude', response.data)  # Ensure that latitude validation error is raised

    def test_latitude_below_min_value(self):
        data = {
            "cadastral_number": "123456",
            "latitude": -91.0,  # Invalid latitude (less than -90)
            "longitude": 45.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('latitude', response.data)

    def test_longitude_above_max_value(self):
        data = {
            "cadastral_number": "123456",
            "latitude": 45.0,
            "longitude": 181.0  # Invalid longitude (greater than 180)
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('longitude', response.data)

    def test_longitude_below_min_value(self):
        data = {
            "cadastral_number": "123456",
            "latitude": 45.0,
            "longitude": -181.0  # Invalid longitude (less than -180)
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('longitude', response.data)

    
class HistoryAPITests(APITestCase):

    def setUp(self):
        # Creating multiple queries to test history
        self.query1 = Query.objects.create(
            cadastral_number='010101', latitude=50.45, longitude=30.523
        )
        self.query2 = Query.objects.create(
            cadastral_number='101010', latitude=48.856, longitude=2.352
        )

    def test_get_history(self):
        """
        Test retrieving the history of queries
        """
        url = reverse('history-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_history_filter(self):
        """
        Test retrieving history with filter by cadastral number
        """
        url = reverse('history-list')
        response = self.client.get(url, {'cadastral_number': '101010'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),4)
        self.assertEqual(response.data.get('results')[0]['cadastral_number'], '101010')
   
class PingAPITests(APITestCase):

    def test_ping(self):
        """
        Test the ping endpoint to check if the service is running
        """
        url = reverse('ping-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "The service is up and running")
        self.assertIn('version', response.data)