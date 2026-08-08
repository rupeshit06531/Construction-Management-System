from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.employees.models import Employee
from apps.payroll.models import Payroll


class PayrollAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="payroll_admin",
            email="payroll@test.com",
            password="password123",
            role="ADMIN",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.employee = Employee.objects.create(
            first_name="Rahul",
            last_name="Kumar",
            employee_type="WORKER",
            phone="9999999999",
            joining_date="2026-01-01",
            salary=15000,
        )

    def create_payroll(self):
        return Payroll.objects.create(
            employee=self.employee,
            month="2026-01-01",
            basic_salary=15000,
            bonus=1000,
            deduction=500,
            net_salary=15500,
            status="PENDING",
            remarks="January 2026 payroll",
        )

    def test_payroll_list(self):
        self.create_payroll()

        response = self.client.get(
            "/api/payroll/"
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
            "Rahul Kumar",
        )

        self.assertEqual(
            response.data["results"][0]["status"],
            "PENDING",
        )

    def test_payroll_create(self):
        response = self.client.post(
            "/api/payroll/",
            {
                "employee": self.employee.id,
                "month": "2026-02-01",
                "basic_salary": "16000.00",
                "bonus": "1500.00",
                "deduction": "500.00",
                "net_salary": "17000.00",
                "status": "PENDING",
                "remarks": "February 2026 payroll",
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
            "Rahul Kumar",
        )

        self.assertEqual(
            response.data["net_salary"],
            "17000.00",
        )

        self.assertTrue(
            Payroll.objects.filter(
                id=response.data["id"]
            ).exists()
        )

    def test_payroll_retrieve(self):
        payroll = self.create_payroll()

        response = self.client.get(
            f"/api/payroll/{payroll.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            payroll.id,
        )

        self.assertEqual(
            response.data["employee_name"],
            "Rahul Kumar",
        )

        self.assertEqual(
            response.data["basic_salary"],
            "15000.00",
        )

        self.assertEqual(
            response.data["net_salary"],
            "15500.00",
        )

        self.assertEqual(
            response.data["status"],
            "PENDING",
        )

    def test_payroll_update(self):
        payroll = self.create_payroll()

        response = self.client.patch(
            f"/api/payroll/{payroll.id}/",
            {
                "bonus": "2000.00",
                "deduction": "1000.00",
                "net_salary": "16000.00",
                "status": "PAID",
                "remarks": "Salary paid",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["bonus"],
            "2000.00",
        )

        self.assertEqual(
            response.data["deduction"],
            "1000.00",
        )

        self.assertEqual(
            response.data["net_salary"],
            "16000.00",
        )

        self.assertEqual(
            response.data["status"],
            "PAID",
        )

        self.assertEqual(
            response.data["remarks"],
            "Salary paid",
        )

    def test_payroll_delete_by_super_admin(self):
        payroll = self.create_payroll()

        super_admin = User.objects.create_user(
            username="payroll_superadmin",
            email="payroll_superadmin@test.com",
            password="password123",
            role="SUPER_ADMIN",
        )

        self.client.force_authenticate(
            user=super_admin
        )

        response = self.client.delete(
            f"/api/payroll/{payroll.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Payroll.objects.filter(
                id=payroll.id
            ).exists()
        )