from datetime import date

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from apps.materials.models import Material
from apps.projects.models import Project


User = get_user_model()


class MaterialAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="material_manager",
            email="material@test.com",
            password="password123",
            role="SUPER_ADMIN",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "material@test.com",
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
            name="Material Project",
            code="MAT001",
            client="Client",
            location="Ranchi",
            start_date=date.today(),
            budget=200000,
            manager=self.user,
        )

    def create_material(self):
        return Material.objects.create(
            project=self.project,
            name="Cement",
            category="CEMENT",
            unit="BAG",
            quantity=100,
            purchase_price=500,
            supplier="ABC Supplier",
        )

    def test_material_list(self):
        self.create_material()

        response = self.client.get(
            "/api/materials/"
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
            response.data["results"][0]["name"],
            "Cement",
        )

        self.assertEqual(
            response.data["results"][0]["project_name"],
            "Material Project",
        )

    def test_material_create(self):
        response = self.client.post(
            "/api/materials/",
            {
                "project": self.project.id,
                "name": "Steel",
                "category": "STEEL",
                "unit": "KG",
                "quantity": "250.00",
                "purchase_price": "75.00",
                "supplier": "Steel Supplier",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["project"],
            self.project.id,
        )

        self.assertEqual(
            response.data["project_name"],
            "Material Project",
        )

        self.assertEqual(
            response.data["name"],
            "Steel",
        )

        self.assertEqual(
            response.data["category"],
            "STEEL",
        )

        self.assertEqual(
            response.data["quantity"],
            "250.00",
        )

        self.assertTrue(
            Material.objects.filter(
                id=response.data["id"]
            ).exists()
        )

    def test_material_retrieve(self):
        material = self.create_material()

        response = self.client.get(
            f"/api/materials/{material.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            material.id,
        )

        self.assertEqual(
            response.data["name"],
            "Cement",
        )

        self.assertEqual(
            response.data["project_name"],
            "Material Project",
        )

        self.assertEqual(
            response.data["quantity"],
            "100.00",
        )

    def test_material_update(self):
        material = self.create_material()

        response = self.client.patch(
            f"/api/materials/{material.id}/",
            {
                "name": "Premium Cement",
                "quantity": "150.00",
                "purchase_price": "550.00",
                "supplier": "Updated Supplier",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["name"],
            "Premium Cement",
        )

        self.assertEqual(
            response.data["quantity"],
            "150.00",
        )

        self.assertEqual(
            response.data["purchase_price"],
            "550.00",
        )

        self.assertEqual(
            response.data["supplier"],
            "Updated Supplier",
        )

    def test_material_delete(self):
        material = self.create_material()

        response = self.client.delete(
            f"/api/materials/{material.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Material.objects.filter(
                id=material.id
            ).exists()
        )