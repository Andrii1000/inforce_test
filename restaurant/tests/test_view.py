from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Restaurant, Menu, Vote
from user.models import Employee
from django.utils import timezone

class RestaurantViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.employee = Employee.objects.create(user=self.user, department="IT")
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", address="123 Main St")
        self.client.login(username="testuser", password="testpass")
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post('/token/', {'username': 'testuser', 'password': 'testpass'}, format='json')
        return response.data['access']

    def test_menu_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'restaurant': self.restaurant.id,
            'dishes': 'Pasta, Burger',
        }
        response = self.client.post('/menus/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dishes'], 'Pasta, Burger')

    def test_today_menu(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get('/menus/today/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vote_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        menu = Menu.objects.create(restaurant=self.restaurant, day=timezone.now().date(), dishes="Sushi")
        vote_data = {
            'menu': menu.id,
        }
        response = self.client.post('/votes/', vote_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vote_duplicate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        vote_data = {
            'menu': self.restaurant.menus.first().id,
        }
        self.client.post('/votes/', vote_data, format='json')
        response = self.client.post('/votes/', vote_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You have already voted', str(response.data))
