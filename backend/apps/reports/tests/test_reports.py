from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.reports.models import Report


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

        self.report_data = {
            "title": "August 2026 Project Report",
            "report_type": "PROJECT",
            "start_date": "2026-08-01",
            "end_date": "2026-08-31",
            "data": {
                "project_name": "Metro Station Project",
                "status": "ACTIVE",
                "location": "Ranchi",
                "budget": "50000000.00",
            },
        }

    def create_report(self):
        return self.client.post(
            "/api/reports/",
            self.report_data,
            format="json",
        )

    def test_dashboard_report(self):
        response = self.client.get(
            "/api/reports/dashboard/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsInstance(
            response.data,
            list,
        )

    def test_create_report(self):
        response = self.create_report()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["title"],
            "August 2026 Project Report",
        )

        self.assertEqual(
            response.data["report_type"],
            "PROJECT",
        )

        self.assertEqual(
            response.data["generated_by"],
            self.user.id,
        )

        self.assertTrue(
            Report.objects.filter(
                id=response.data["id"]
            ).exists()
        )

    def test_list_reports(self):
        self.create_report()

        response = self.client.get(
            "/api/reports/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertEqual(
            len(response.data["results"]),
            1,
        )

    def test_retrieve_report(self):
        create_response = self.create_report()

        report_id = create_response.data["id"]

        response = self.client.get(
            f"/api/reports/{report_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            report_id,
        )

        self.assertEqual(
            response.data["title"],
            "August 2026 Project Report",
        )

    def test_update_report(self):
        create_response = self.create_report()

        report_id = create_response.data["id"]

        response = self.client.patch(
            f"/api/reports/{report_id}/",
            {
                "title": "Updated Project Report",
                "data": {
                    "progress": "25%",
                },
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Updated Project Report",
        )

        self.assertEqual(
            response.data["data"]["progress"],
            "25%",
        )

    def test_delete_report(self):
        create_response = self.create_report()

        report_id = create_response.data["id"]

        response = self.client.delete(
            f"/api/reports/{report_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Report.objects.filter(
                id=report_id
            ).exists()
        )