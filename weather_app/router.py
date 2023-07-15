from rest_framework.routers import DefaultRouter

from .viewset import (
    WeatherDataViewSet,
)

router = DefaultRouter()

router.register(r"weather", WeatherDataViewSet, basename="weather")
