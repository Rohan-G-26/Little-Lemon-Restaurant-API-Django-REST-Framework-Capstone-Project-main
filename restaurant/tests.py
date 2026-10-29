from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Booking, Menu


class MenuAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu = Menu.objects.create(title="Greek Salad", price="12.50", inventory=10)

    def test_list_menu_is_public(self):
        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Greek Salad", str(response.data))

    def test_create_menu_requires_authentication(self):
        response = self.client.post("/api/menu/", {"title": "Pasta", "price": "14.00", "inventory": 5}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_create_menu(self):
        user = get_user_model().objects.create_user(username="chef", password="SafePass123!")
        self.client.force_authenticate(user=user)
        response = self.client.post("/api/menu/", {"title": "Pasta", "price": "14.00", "inventory": 5}, format="json")
        self.assertEqual(response.status_code, 201)


class BookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {"first_name": "Ada", "reservation_date": (date.today() + timedelta(days=1)).isoformat(), "reservation_slot": 18}

    def test_create_booking(self):
        response = self.client.post("/api/booking/tables/", self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)

    def test_duplicate_date_and_slot_is_rejected(self):
        self.client.post("/api/booking/tables/", self.payload, format="json")
        response = self.client.post("/api/booking/tables/", {**self.payload, "first_name": "Grace"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_past_date_is_rejected(self):
        payload = {**self.payload, "reservation_date": (date.today() - timedelta(days=1)).isoformat()}
        response = self.client.post("/api/booking/tables/", payload, format="json")
        self.assertEqual(response.status_code, 400)


class AuthenticationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        response = self.client.post("/api/auth/register/", {"username": "learner", "email": "learner@example.com", "password": "StrongPass123!"}, format="json")
        self.assertEqual(response.status_code, 201)

    def test_login_returns_token(self):
        get_user_model().objects.create_user(username="learner", password="StrongPass123!")
        response = self.client.post("/api/auth/token/", {"username": "learner", "password": "StrongPass123!"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
