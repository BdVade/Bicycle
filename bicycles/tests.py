from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from .models import Bicycle


# Create your tests here.
class BicycleTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('testuser', email='testuser@test.com', password='testing')
        self.user.save()
        url = reverse('jwt-create')
        resp = self.client.post(url, {'username': 'testuser', 'password': 'testing'}, format='json')
        self.token = resp.data['access']


    def test_unauthenticated_create_bicycle(self):
        url = reverse("bicycles_list_and_create")
        data = {"name": "random", "description": "random"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_create_bicycle(self):
        url = reverse("bicycles_list_and_create")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {"name": "random", "description": "Nice bike"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("name"), "random")
        self.assertEqual(response.data.get("description"), "Nice bike")
        count = Bicycle.objects.count()
        bike = Bicycle.objects.get(id=1)
        self.assertEqual(count, 1)
        self.assertEqual(bike.name, data.get('name'))


    def test_unauthenticated_list_bicycle(self):
        url = reverse("bicycles_list_and_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_list_bicycle(self):
        Bicycle.objects.create(name="Raleigh", description="Nice")
        url = reverse("bicycles_list_and_create")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(1, len(response.data))
        self.assertEqual(response.data[0].get('name'), 'Raleigh')

