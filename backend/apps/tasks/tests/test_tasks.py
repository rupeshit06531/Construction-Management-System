from datetime import date

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from apps.employees.models import Employee
from apps.projects.models import Project
from apps.tasks.models import Task


User = get_user_model()


class TaskAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="task_manager",
            email="task@test.com",
            password="password123",
            role="SUPER_ADMIN",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "task@test.com",
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

        self.project = Project.objects.create(
            name="Task Project",
            code="TASK001",
            client="Client",
            location="Ranchi",
            start_date=date.today(),
            budget=300000,
            manager=self.user,
        )

        self.employee = Employee.objects.create(
            first_name="Amit",
            last_name="Kumar",
            employee_type="ENGINEER",
            phone="8888888888",
            joining_date=date.today(),
            salary=25000,
        )

    def create_task(self):
        return Task.objects.create(
            project=self.project,
            assigned_to=self.employee,
            title="Foundation Work",
            description="Complete foundation work",
            priority="HIGH",
            status="PENDING",
            start_date=date.today(),
            completion_percentage=0,
        )

    def test_task_list(self):
        self.create_task()

        response = self.client.get(
            "/api/tasks/"
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
            response.data["results"][0]["title"],
            "Foundation Work",
        )

        self.assertEqual(
            response.data["results"][0]["project_name"],
            "Task Project",
        )

        self.assertEqual(
            response.data["results"][0]["assigned_to_name"],
            str(self.employee),
        )

    def test_task_create(self):
        response = self.client.post(
            "/api/tasks/",
            {
                "project": self.project.id,
                "assigned_to": self.employee.id,
                "title": "Column Work",
                "description": "Complete column work",
                "priority": "MEDIUM",
                "status": "PENDING",
                "start_date": str(date.today()),
                "end_date": "2026-08-31",
                "completion_percentage": 10,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["project"],
            self.project.id,
        )

        self.assertEqual(
            response.data["assigned_to"],
            self.employee.id,
        )

        self.assertEqual(
            response.data["title"],
            "Column Work",
        )

        self.assertEqual(
            response.data["priority"],
            "MEDIUM",
        )

        self.assertEqual(
            response.data["completion_percentage"],
            10,
        )

        self.assertTrue(
            Task.objects.filter(
                id=response.data["id"]
            ).exists()
        )

    def test_task_retrieve(self):
        task = self.create_task()

        response = self.client.get(
            f"/api/tasks/{task.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            task.id,
        )

        self.assertEqual(
            response.data["title"],
            "Foundation Work",
        )

        self.assertEqual(
            response.data["project_name"],
            "Task Project",
        )

        self.assertEqual(
            response.data["assigned_to_name"],
            str(self.employee),
        )

    def test_task_update(self):
        task = self.create_task()

        response = self.client.patch(
            f"/api/tasks/{task.id}/",
            {
                "title": "Updated Foundation Work",
                "status": "IN_PROGRESS",
                "priority": "HIGH",
                "completion_percentage": 50,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Updated Foundation Work",
        )

        self.assertEqual(
            response.data["status"],
            "IN_PROGRESS",
        )

        self.assertEqual(
            response.data["priority"],
            "HIGH",
        )

        self.assertEqual(
            response.data["completion_percentage"],
            50,
        )

    def test_task_delete(self):
        task = self.create_task()

        response = self.client.delete(
            f"/api/tasks/{task.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Task.objects.filter(
                id=task.id
            ).exists()
        )