from datetime import date, time

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from apps.attendance.models import Attendance
from apps.employees.models import Employee


User = get_user_model()


class AttendanceAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="attendance_manager",
            email="attendance@test.com",
            password="password123",
            role="SUPER_ADMIN",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "attendance@test.com",
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

        self.employee = Employee.objects.create(
            first_name="Rahul",
            last_name="Kumar",
            employee_type="WORKER",
            phone="9999999999",
            joining_date=date.today(),
            salary=15000,
        )

    def create_attendance(self):
        return Attendance.objects.create(
            employee=self.employee,
            date=date.today(),
            status="PRESENT",
            check_in=time(9, 0),
            check_out=time(18, 0),
            remarks="Regular attendance",
        )

    def test_attendance_list(self):
        self.create_attendance()

        response = self.client.get(
            "/api/attendance/"
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
            response.data["results"][0]["employee"],
            self.employee.id,
        )

        self.assertEqual(
            response.data["results"][0]["employee_name"],
            str(self.employee),
        )

        self.assertEqual(
            response.data["results"][0]["status"],
            "PRESENT",
        )

    def test_attendance_create(self):
        response = self.client.post(
            "/api/attendance/",
            {
                "employee": self.employee.id,
                "date": str(date.today()),
                "status": "PRESENT",
                "check_in": "09:00:00",
                "check_out": "18:00:00",
                "remarks": "Regular attendance",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["employee"],
            self.employee.id,
        )

        self.assertEqual(
            response.data["employee_name"],
            str(self.employee),
        )

        self.assertEqual(
            response.data["status"],
            "PRESENT",
        )

        self.assertTrue(
            Attendance.objects.filter(
                id=response.data["id"]
            ).exists()
        )

    def test_attendance_retrieve(self):
        attendance = self.create_attendance()

        response = self.client.get(
            f"/api/attendance/{attendance.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            attendance.id,
        )

        self.assertEqual(
            response.data["employee_name"],
            str(self.employee),
        )

        self.assertEqual(
            response.data["status"],
            "PRESENT",
        )

        self.assertEqual(
            response.data["check_in"],
            "09:00:00",
        )

        self.assertEqual(
            response.data["check_out"],
            "18:00:00",
        )

    def test_attendance_update(self):
        attendance = self.create_attendance()

        response = self.client.patch(
            f"/api/attendance/{attendance.id}/",
            {
                "status": "LEAVE",
                "remarks": "Approved leave",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["status"],
            "LEAVE",
        )

        self.assertEqual(
            response.data["remarks"],
            "Approved leave",
        )

    def test_attendance_delete(self):
        attendance = self.create_attendance()

        response = self.client.delete(
            f"/api/attendance/{attendance.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Attendance.objects.filter(
                id=attendance.id
            ).exists()
        )