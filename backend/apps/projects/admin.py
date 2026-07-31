from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
        "client",
        "manager",
        "status",
        "start_date",
        "end_date",
        "budget",
        "created_at",
    )

    list_filter = (
        "status",
        "start_date",
        "created_at",
    )

    search_fields = (
        "code",
        "name",
        "client",
        "location",
        "manager__username",
        "manager__email",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Project Information",
            {
                "fields": (
                    "name",
                    "code",
                    "description",
                    "status",
                )
            },
        ),
        (
            "Client Information",
            {
                "fields": (
                    "client",
                    "location",
                )
            },
        ),
        (
            "Project Planning",
            {
                "fields": (
                    "manager",
                    "start_date",
                    "end_date",
                    "budget",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )