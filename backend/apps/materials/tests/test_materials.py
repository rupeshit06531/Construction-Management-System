from datetime import date

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from apps.projects.models import Project
from apps.materials.models import Material


User = get_user_model()


class MaterialAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="material_manager",
            email="material@test.com",
            password="password123",
            role="MANAGER",
        )

        response = self.client.post(
            "/api/accounts/login/",
            {
                "email": "material@test.com",
                "password": "password123",
            },
            format="json",
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


    def test_material_list(self):

        Material.objects.create(
            project=self.project,
            name="Cement",
            category="CEMENT",
            unit="BAG",
            quantity=100,
            purchase_price=500,
        )

        response = self.client.get(
            "/api/materials/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )