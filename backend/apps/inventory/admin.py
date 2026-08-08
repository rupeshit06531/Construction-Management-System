from django.contrib import admin

from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "material",
        "transaction_type",
        "quantity",
        "created_at",
    ]

    list_filter = [
        "transaction_type",
    ]

    search_fields = [
        "material__name",
    ]