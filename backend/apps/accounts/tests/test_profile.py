from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class ProfileAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="profileuser",
            email="profile@test.com",
            password="password123",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "profile@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )


    def test_current_user_profile(self):

        response = self.client.get(
            "/api/accounts/me/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )