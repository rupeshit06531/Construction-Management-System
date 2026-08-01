from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class DashboardAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="dashboard_user",
            email="dashboard@test.com",
            password="password123",
            role="MANAGER",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "dashboard@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )


    def test_dashboard_summary(self):

        response = self.client.get(
            "/api/dashboard/kpi/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )