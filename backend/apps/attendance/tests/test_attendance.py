from datetime import date

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from apps.employees.models import Employee
from apps.attendance.models import Attendance


User = get_user_model()


class AttendanceAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="attendance_manager",
            email="attendance@test.com",
            password="password123",
            role="MANAGER",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "attendance@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.employee = Employee.objects.create(
            first_name="Rahul",
            last_name="Kumar",
            employee_type="WORKER",
            phone="9999999999",
            joining_date=date.today(),
            salary=15000,
        )


    def test_attendance_list(self):

        Attendance.objects.create(
            employee=self.employee,
            date=date.today(),
            status="PRESENT",
        )

        response = self.client.get(
            "/api/attendance/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )