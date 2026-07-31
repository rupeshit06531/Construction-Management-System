from django.contrib import admin
from django.urls import include, path


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
]