from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from announcement.models import Category

class UserCreatePostTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/accounts/seller/registration/"
        self.category = Category.objects.filter(id=3)

    def test_create_post(self):
        data = {'username': 'Dipper', 'product': 'Notebook', 'phone_number': '+998975668458', 'category': self.category, 'address': 'Chilonzor, Tashkent'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

