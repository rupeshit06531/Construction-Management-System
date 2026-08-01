from rest_framework.test import APITestCase
from rest_framework import status

from apps.accounts.models import User


class ReportsAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="password123",
            role="ADMIN",
        )

        self.client.force_authenticate(
            user=self.user
        )


    def test_dashboard_report(self):

        url = "/api/reports/dashboard/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIsInstance(
            response.data,
            list
        )