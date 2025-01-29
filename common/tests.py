from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class RegionAndDistrictsListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient
        self.url = '/api/common/regions-with-districts/'

    def test_list_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StaticPageGetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient
        self.url = '/api/common/pages/<slug:Static Page slug>/'

    def test_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)