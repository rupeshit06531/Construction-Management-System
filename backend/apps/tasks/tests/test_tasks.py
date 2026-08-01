from datetime import date

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from apps.projects.models import Project
from apps.employees.models import Employee
from apps.tasks.models import Task


User = get_user_model()


class TaskAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="task_manager",
            email="task@test.com",
            password="password123",
            role="MANAGER",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "task@test.com",
                "password": "password123",
            },
            format="json",
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


    def test_task_list(self):

        Task.objects.create(
            project=self.project,
            assigned_to=self.employee,
            title="Foundation Work",
            description="Complete foundation work",
            priority="HIGH",
            status="PENDING",
        )


        response = self.client.get(
            "/api/tasks/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )