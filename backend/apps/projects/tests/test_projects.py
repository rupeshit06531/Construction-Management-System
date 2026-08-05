from datetime import date

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from apps.projects.models import Project


User = get_user_model()


class ProjectAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="manager",
            email="manager@test.com",
            password="password123",
            role="MANAGER",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "manager@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

    def test_project_list(self):

        Project.objects.create(
            name="Test Building",
            code="PRJ001",
            client="ABC Client",
            location="Ranchi",
            start_date=date.today(),
            budget=100000,
            manager=self.user,
        )

        response = self.client.get(
            "/api/projects/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_project_list_pagination(self):

        for index in range(25):
            Project.objects.create(
                name=f"Test Building {index}",
                code=f"PRJ{index + 100:03d}",
                client="ABC Client",
                location="Ranchi",
                start_date=date.today(),
                budget=100000,
                manager=self.user,
            )

        response = self.client.get(
            "/api/projects/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "count",
            response.data,
        )

        self.assertIn(
            "next",
            response.data,
        )

        self.assertIn(
            "previous",
            response.data,
        )

        self.assertIn(
            "results",
            response.data,
        )

        self.assertEqual(
            response.data["count"],
            25,
        )

        self.assertEqual(
            len(response.data["results"]),
            20,
        )

        self.assertIsNotNone(
            response.data["next"],
        )

        self.assertIsNone(
            response.data["previous"],
        )