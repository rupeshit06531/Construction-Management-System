from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class PasswordChangeAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="passworduser",
            email="password@test.com",
            password="oldpassword123",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "password@test.com",
                "password": "oldpassword123",
            },
            format="json",
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )


    def test_password_change(self):

        response = self.client.post(
            "/api/accounts/password/change/",
            {
                "old_password": "oldpassword123",
                "new_password": "newpassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )