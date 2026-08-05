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
            first_name="Rupesh",
            last_name="Mahto",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "manager@test.com",
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

    def create_project(self):
        return Project.objects.create(
            name="Test Building",
            code="PRJ001",
            description="Construction project",
            client="ABC Client",
            location="Ranchi",
            start_date=date(2026, 8, 1),
            end_date=date(2027, 12, 31),
            budget=100000,
            status="ACTIVE",
            manager=self.user,
        )

    def test_project_list(self):
        self.create_project()

        response = self.client.get(
            "/api/projects/"
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

        self.assertEqual(
            response.data["results"][0]["name"],
            "Test Building",
        )

        self.assertEqual(
            response.data["results"][0]["manager"],
            self.user.id,
        )

        self.assertEqual(
            response.data["results"][0]["manager_name"],
            "Rupesh Mahto",
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

    def test_project_create(self):
        response = self.client.post(
            "/api/projects/",
            {
                "name": "Metro Station Project",
                "code": "METRO001",
                "description": "Construction of metro station",
                "client": "ABC Infrastructure Ltd",
                "location": "Ranchi",
                "start_date": "2026-08-01",
                "end_date": "2027-12-31",
                "budget": "50000000.00",
                "status": "ACTIVE",
                "manager": self.user.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["name"],
            "Metro Station Project",
        )

        self.assertEqual(
            response.data["code"],
            "METRO001",
        )

        self.assertEqual(
            response.data["manager"],
            self.user.id,
        )

        self.assertEqual(
            response.data["manager_name"],
            "Rupesh Mahto",
        )

        self.assertTrue(
            Project.objects.filter(
                id=response.data["id"]
            ).exists()
        )

    def test_project_retrieve(self):
        project = self.create_project()

        response = self.client.get(
            f"/api/projects/{project.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            project.id,
        )

        self.assertEqual(
            response.data["name"],
            "Test Building",
        )

        self.assertEqual(
            response.data["code"],
            "PRJ001",
        )

        self.assertEqual(
            response.data["manager_name"],
            "Rupesh Mahto",
        )

    def test_project_update(self):
        project = self.create_project()

        response = self.client.patch(
            f"/api/projects/{project.id}/",
            {
                "name": "Updated Building",
                "budget": "250000.00",
                "status": "COMPLETED",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["name"],
            "Updated Building",
        )

        self.assertEqual(
            response.data["budget"],
            "250000.00",
        )

        self.assertEqual(
            response.data["status"],
            "COMPLETED",
        )

    def test_project_date_validation(self):
        response = self.client.post(
            "/api/projects/",
            {
                "name": "Invalid Project",
                "code": "INVALID001",
                "client": "ABC Client",
                "location": "Ranchi",
                "start_date": "2027-01-01",
                "end_date": "2026-01-01",
                "budget": "100000.00",
                "status": "PLANNING",
                "manager": self.user.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "end_date",
            response.data["errors"],

        )

    def test_project_delete(self):
        project = self.create_project()

        response = self.client.delete(
            f"/api/projects/{project.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Project.objects.filter(
                id=project.id
            ).exists()
        )