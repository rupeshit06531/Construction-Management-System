from datetime import date

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from apps.expenses.models import Expense
from apps.projects.models import Project


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

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
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

    def create_expense(self):
        return Expense.objects.create(
            project=self.project,
            title="Cement Purchase",
            category="MATERIAL",
            amount=25000,
            expense_date=date.today(),
            description="Cement purchase for project",
        )

    def test_expense_list(self):
        self.create_expense()

        response = self.client.get(
            "/api/expenses/"
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
            "Cement Purchase",
        )

        self.assertEqual(
            response.data["results"][0]["project"],
            self.project.id,
        )

        self.assertEqual(
            response.data["results"][0]["project_name"],
            "Expense Project",
        )

    def test_expense_create(self):
        response = self.client.post(
            "/api/expenses/",
            {
                "project": self.project.id,
                "title": "Labour Payment",
                "category": "LABOUR",
                "amount": "15000.00",
                "expense_date": str(date.today()),
                "description": "Labour expense",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["title"],
            "Labour Payment",
        )

        self.assertEqual(
            response.data["category"],
            "LABOUR",
        )

        self.assertEqual(
            response.data["project_name"],
            "Expense Project",
        )

        self.assertTrue(
            Expense.objects.filter(
                id=response.data["id"]
            ).exists()
        )

    def test_expense_retrieve(self):
        expense = self.create_expense()

        response = self.client.get(
            f"/api/expenses/{expense.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            expense.id,
        )

        self.assertEqual(
            response.data["title"],
            "Cement Purchase",
        )

        self.assertEqual(
            response.data["amount"],
            "25000.00",
        )

        self.assertEqual(
            response.data["project_name"],
            "Expense Project",
        )

    def test_expense_update(self):
        expense = self.create_expense()

        response = self.client.patch(
            f"/api/expenses/{expense.id}/",
            {
                "title": "Updated Cement Purchase",
                "amount": "30000.00",
                "description": "Updated expense",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Updated Cement Purchase",
        )

        self.assertEqual(
            response.data["amount"],
            "30000.00",
        )

        self.assertEqual(
            response.data["description"],
            "Updated expense",
        )

    def test_expense_delete_by_super_admin(self):
        expense = self.create_expense()

        super_admin = User.objects.create_user(
            username="expense_superadmin",
            email="expense_superadmin@test.com",
            password="password123",
            role="SUPER_ADMIN",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "expense_superadmin@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {response.data['access']}"
            )
        )

        response = self.client.delete(
            f"/api/expenses/{expense.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Expense.objects.filter(
                id=expense.id
            ).exists()
        )