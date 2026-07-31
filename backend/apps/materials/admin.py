from django.contrib import admin

from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "name",
        "category",
        "quantity",
        "unit",
        "purchase_price",
        "project",
        "supplier",
        "created_at",
    ]

    list_filter = [
        "category",
        "project",
    ]

    search_fields = [
        "name",
        "supplier",
    ]