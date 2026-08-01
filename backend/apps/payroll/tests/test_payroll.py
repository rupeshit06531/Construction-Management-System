from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.employees.models import Employee
from apps.payroll.models import Payroll


class PayrollAPITest(APITestCase):

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

        self.employee = Employee.objects.create(
            first_name="Rahul",
            last_name="Kumar",
            employee_type="WORKER",
            phone="9999999999",
            joining_date="2026-01-01",
            salary=15000,
        )

        self.payroll = Payroll.objects.create(
            employee=self.employee,
            month="2026-01-01",
            basic_salary=15000,
            bonus=1000,
            deduction=500,
            net_salary=15500,
        )


    def test_payroll_list(self):

        url = "/api/payroll/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )