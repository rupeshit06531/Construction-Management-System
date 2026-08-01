from datetime import date

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from apps.employees.models import Employee


User = get_user_model()


class EmployeeAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="employee_manager",
            email="employee@test.com",
            password="password123",
            role="MANAGER",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "employee@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )


    def test_employee_list(self):

        Employee.objects.create(
            first_name="Raj",
            last_name="Kumar",
            employee_type="ENGINEER",
            phone="9876543210",
            email="raj@test.com",
            joining_date=date.today(),
            salary=50000,
        )

        response = self.client.get(
            "/api/employees/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )