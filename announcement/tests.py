from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class CategoryGetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/store/categories/with/children/'

    def test_list_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchGetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/store/search/complete/'

    def test_get(self):
        data = {'q':'something'}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductCreateTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/store/ads/create/'

    def test_create_post(self):
        data = {'name': 'Product name', 'sub_category': 'Category id', 'author': 'Author full username', 'price': 'product price', 'currency': 'product currency', 'description': 'product description', 'phone_number': 'author phone number', 'address': 'author address'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProductListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/store/ads/list/'

    def test_list_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductUpdateTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/store/ads/update/<slug:product slug>"

    def test_update(self):
        data = {'name': 'Product name', 'sub_category': 'Category id', 'author': 'Author full username', 'price': 'product price', 'currency': 'product currency', 'description': 'product description', 'phone_number': 'author phone number', 'address': 'author address'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/store/ads/<slug:product slug>'

    def test_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductDeleteTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/store/ads/destroy/<slug:product slug>'

    def test_delete(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PopularSearchGetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/store/search/populars/'

    def test_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)