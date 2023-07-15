from django.db import models


# Create your models here.
class WeatherData(models.Model):
    latitude = models.DecimalField(
        max_digits=15,
        decimal_places=9,
    )
    longitude = models.DecimalField(
        max_digits=15,
        decimal_places=9,
    )
    detailing_type = models.CharField(
        max_length=20,
    )
    data = models.JSONField(
        blank=True,
        null=True,
    )
    timestamp = models.DateTimeField(
        auto_now=True,
    )
