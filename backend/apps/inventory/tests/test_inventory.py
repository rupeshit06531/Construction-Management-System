from datetime import date

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from apps.inventory.models import Inventory
from apps.materials.models import Material
from apps.projects.models import Project


User = get_user_model()


class InventoryAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="inventory_manager",
            email="inventory@test.com",
            password="password123",
            role="SUPER_ADMIN",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "inventory@test.com",
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

    def create_inventory(self):
        return Inventory.objects.create(
            material=self.material,
            transaction_type="IN",
            quantity=100,
            remarks="Initial stock",
        )

    def test_inventory_list(self):
        self.create_inventory()

        response = self.client.get(
            "/api/inventory/"
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
            response.data["results"][0]["material_name"],
            "Cement",
        )

    def test_inventory_create(self):
        response = self.client.post(
            "/api/inventory/",
            {
                "material": self.material.id,
                "transaction_type": "IN",
                "quantity": "50.00",
                "remarks": "New cement stock",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["material"],
            self.material.id,
        )

        self.assertEqual(
            response.data["material_name"],
            "Cement",
        )

        self.assertEqual(
            response.data["transaction_type"],
            "IN",
        )

        self.assertEqual(
            response.data["quantity"],
            "50.00",
        )

        self.assertTrue(
            Inventory.objects.filter(
                id=response.data["id"]
            ).exists()
        )

    def test_inventory_retrieve(self):
        inventory = self.create_inventory()

        response = self.client.get(
            f"/api/inventory/{inventory.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            inventory.id,
        )

        self.assertEqual(
            response.data["material_name"],
            "Cement",
        )

        self.assertEqual(
            response.data["quantity"],
            "100.00",
        )

    def test_inventory_update(self):
        inventory = self.create_inventory()

        response = self.client.patch(
            f"/api/inventory/{inventory.id}/",
            {
                "transaction_type": "OUT",
                "quantity": "25.00",
                "remarks": "Material issued",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["transaction_type"],
            "OUT",
        )

        self.assertEqual(
            response.data["quantity"],
            "25.00",
        )

        self.assertEqual(
            response.data["remarks"],
            "Material issued",
        )

    def test_inventory_delete(self):
        inventory = self.create_inventory()

        response = self.client.delete(
            f"/api/inventory/{inventory.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Inventory.objects.filter(
                id=inventory.id
            ).exists()
        )