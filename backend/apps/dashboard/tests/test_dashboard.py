from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase


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

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

    def test_dashboard_kpi(self):
        response = self.client.get(
            "/api/dashboard/kpi/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "total_projects",
            response.data,
        )

        self.assertIn(
            "total_employees",
            response.data,
        )

        self.assertIn(
            "total_tasks",
            response.data,
        )

        self.assertIn(
            "total_materials",
            response.data,
        )

        self.assertIn(
            "total_inventory_items",
            response.data,
        )

        self.assertIn(
            "total_expenses",
            response.data,
        )

        self.assertIn(
            "total_payroll",
            response.data,
        )

    def test_monthly_expenses(self):
        response = self.client.get(
            "/api/dashboard/monthly-expenses/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsInstance(
            response.data,
            list,
        )