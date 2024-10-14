from django.test import TestCase
from django.contrib.auth.models import User
from restaurant.models import Restaurant, Menu, Vote
from user.models import Employee
from django.utils import timezone

class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", address="123 Main St", description="Test Description")

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, "Test Restaurant")
        self.assertEqual(self.restaurant.address, "123 Main St")
        self.assertEqual(self.restaurant.description, "Test Description")

class MenuModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", address="123 Main St")
        self.menu = Menu.objects.create(restaurant=self.restaurant, day=timezone.now().date(), dishes="Pizza, Salad")

    def test_menu_creation(self):
        self.assertEqual(self.menu.restaurant.name, "Test Restaurant")
        self.assertEqual(self.menu.dishes, "Pizza, Salad")
        self.assertEqual(self.menu.day, timezone.now().date())

class VoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.employee = Employee.objects.create(user=self.user, department="IT")
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", address="123 Main St")
        self.menu = Menu.objects.create(restaurant=self.restaurant, day=timezone.now().date(), dishes="Pizza, Salad")
        self.vote = Vote.objects.create(employee=self.employee, menu=self.menu)

    def test_vote_creation(self):
        self.assertEqual(self.vote.employee.user.username, "testuser")
        self.assertEqual(self.vote.menu.restaurant.name, "Test Restaurant")
        self.assertEqual(self.vote.menu.dishes, "Pizza, Salad")
