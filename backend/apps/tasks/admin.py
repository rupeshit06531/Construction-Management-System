from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "title",
        "project",
        "assigned_to",
        "priority",
        "status",
        "completion_percentage",
        "created_at",
    ]

    list_filter = [
        "priority",
        "status",
    ]

    search_fields = [
        "title",
        "project__name",
        "assigned_to__first_name",
        "assigned_to__last_name",
    ]