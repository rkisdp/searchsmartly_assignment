from django.db import models


class PointOfInterest(models.Model):
    internal_id = models.AutoField(verbose_name="PoI internal ID", primary_key=True)
    name = models.CharField(verbose_name="PoI name", max_length=256)
    external_id = models.CharField(verbose_name="PoI external ID", max_length=64)
    category = models.CharField(verbose_name="PoI category", max_length=32)
    average_rating = models.DecimalField(verbose_name="Avg. rating", default=0, decimal_places=2, max_digits=10)
    description = models.TextField(verbose_name="PoI description", null=True, blank=True)
    latitude = models.DecimalField(verbose_name="PoI latitude", max_digits=22, decimal_places=16)
    longitude = models.DecimalField(verbose_name="PoI longitude", max_digits=22, decimal_places=16)

    def __str__(self):
        return f"{self.internal_id} - {self.name}"
