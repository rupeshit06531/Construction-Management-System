from datetime import date

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from apps.projects.models import Project
from apps.expenses.models import Expense


User = get_user_model()


class ExpenseAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="expense_manager",
            email="expense@test.com",
            password="password123",
            role="MANAGER",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "expense@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.project = Project.objects.create(
            name="Expense Project",
            code="EXP001",
            client="Client",
            location="Ranchi",
            start_date=date.today(),
            budget=500000,
            manager=self.user,
        )


    def test_expense_list(self):

        Expense.objects.create(
            project=self.project,
            title="Cement Purchase",
            category="MATERIAL",
            amount=25000,
            expense_date=date.today(),
        )

        response = self.client.get(
            "/api/expenses/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )