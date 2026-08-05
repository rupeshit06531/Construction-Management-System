from datetime import date

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

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

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

    def create_employee(self):
        return Employee.objects.create(
            first_name="Raj",
            last_name="Kumar",
            employee_type="ENGINEER",
            phone="9876543210",
            email="raj@test.com",
            joining_date=date(2026, 1, 1),
            salary=50000,
            address="Ranchi",
        )

    def test_employee_list(self):

        self.create_employee()

        response = self.client.get(
            "/api/employees/"
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
            response.data["results"][0]["first_name"],
            "Raj",
        )

    def test_employee_create(self):

        response = self.client.post(
            "/api/employees/",
            {
                "first_name": "Amit",
                "last_name": "Kumar",
                "employee_type": "WORKER",
                "phone": "9999999999",
                "email": "amit@test.com",
                "joining_date": "2026-08-01",
                "salary": "25000.00",
                "address": "Ranchi",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["first_name"],
            "Amit",
        )

        self.assertEqual(
            response.data["employee_type"],
            "WORKER",
        )

        self.assertTrue(
            Employee.objects.filter(
                id=response.data["id"]
            ).exists()
        )

    def test_employee_retrieve(self):

        employee = self.create_employee()

        response = self.client.get(
            f"/api/employees/{employee.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            employee.id,
        )

        self.assertEqual(
            response.data["first_name"],
            "Raj",
        )

        self.assertEqual(
            response.data["email"],
            "raj@test.com",
        )

    def test_employee_update(self):

        employee = self.create_employee()

        response = self.client.patch(
            f"/api/employees/{employee.id}/",
            {
                "first_name": "Rahul",
                "salary": "55000.00",
                "employee_type": "SUPERVISOR",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["first_name"],
            "Rahul",
        )

        self.assertEqual(
            response.data["salary"],
            "55000.00",
        )

        self.assertEqual(
            response.data["employee_type"],
            "SUPERVISOR",
        )

    def test_employee_search(self):

        self.create_employee()

        Employee.objects.create(
            first_name="Amit",
            last_name="Singh",
            employee_type="WORKER",
            phone="8888888888",
            email="amit@test.com",
            joining_date=date(2026, 2, 1),
            salary=25000,
        )

        response = self.client.get(
            "/api/employees/?search=Raj"
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
            response.data["results"][0]["first_name"],
            "Raj",
        )

    def test_employee_delete_forbidden_for_manager(self):

        employee = self.create_employee()

        response = self.client.delete(
            f"/api/employees/{employee.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Employee.objects.filter(
                id=employee.id
            ).exists()
        )