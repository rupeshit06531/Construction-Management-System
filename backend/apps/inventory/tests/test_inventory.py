from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from apps.materials.models import Material
from apps.inventory.models import Inventory

from datetime import date

from apps.projects.models import Project

User = get_user_model()


class InventoryAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="inventory_manager",
            email="inventory@test.com",
            password="password123",
            role="MANAGER",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "inventory@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.project = Project.objects.create(
            name="Inventory Project",
            code="INV001",
            client="Client",
            location="Ranchi",
            start_date=date.today(),
            budget=100000,
            manager=self.user,
        )

        self.material = Material.objects.create(
            project=self.project,
            name="Cement",
            unit="BAG",
            purchase_price=500,
        )


    def test_inventory_list(self):

        Inventory.objects.create(
            material=self.material,
            transaction_type="IN",
            quantity=100,
        )

        response = self.client.get(
            "/api/inventory/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )