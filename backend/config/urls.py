from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/accounts/",
        include("apps.accounts.urls"),
    ),

    path(
        "api/projects/",
        include("apps.projects.urls"),
    ),

    path(
        "api/employees/",
        include("apps.employees.urls"),
    ),

    path(
        "api/tasks/",
        include("apps.tasks.urls"),
    ),

    path(
        "api/materials/",
        include("apps.materials.urls"),
    ),

    path(
        "api/inventory/",
        include("apps.inventory.urls"),
    ),

    path(
        "api/attendance/",
        include("apps.attendance.urls"),
    ),

    path(
        "api/expenses/",
        include("apps.expenses.urls"),
    ),

    path(
        "api/payroll/",
        include("apps.payroll.urls"),
    ),

    path(
        "api/reports/",
        include("apps.reports.urls"),
    ),

    path(
        "api/dashboard/",
        include("apps.dashboard.urls"),
    ),

    path(
        "api/accounts/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

        path(
            "api/schema/",
            SpectacularAPIView.as_view(),
            name="schema",
        ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc",
    ),
]