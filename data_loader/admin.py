from django.contrib import admin
from .models import PointOfInterest


@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_filter = (
        "category",
    )
    search_fields = (
        "external_id",
        "internal_id",
    )
    list_display = (
        "internal_id", "name",
        "external_id", "category",
        "average_rating"
    )

