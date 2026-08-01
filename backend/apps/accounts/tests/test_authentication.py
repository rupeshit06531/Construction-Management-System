from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationAPITest(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")

        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@12345",
            "first_name": "Test",
            "last_name": "User",
            "phone": "9876543210",
        }

        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="Test@12345",
        )

    def test_register_success(self):
        response = self.client.post(
            self.register_url,
            self.user_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                email="test@example.com"
            ).exists()
        )

    def test_register_duplicate_email(self):
        data = self.user_data.copy()
        data["email"] = "existing@example.com"

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "existing@example.com",
                "password": "Test@12345",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_password(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "existing@example.com",
                "password": "WrongPassword",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )