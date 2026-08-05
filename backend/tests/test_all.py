from rest_framework import status
from rest_framework.test import APITestCase


class APIDocumentationTest(APITestCase):

    def test_openapi_schema_endpoint(self):

        response = self.client.get(
            "/api/schema/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "application/vnd.oai.openapi",
            response["Content-Type"],
        )


from apps.accounts.tests.test_authentication import *
from apps.accounts.tests.test_profile import *
from apps.accounts.tests.test_password import *

from apps.projects.tests.test_projects import *

from apps.employees.tests.test_employees import *

from apps.tasks.tests.test_tasks import *

from apps.materials.tests.test_materials import *

from apps.inventory.tests.test_inventory import *

from apps.attendance.tests.test_attendance import *

from apps.expenses.tests.test_expenses import *

from apps.payroll.tests.test_payroll import *

from apps.reports.tests.test_reports import *

from apps.dashboard.tests.test_dashboard import *