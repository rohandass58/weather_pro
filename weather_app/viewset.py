from rest_framework import viewsets
from rest_framework.response import Response
from datetime import timedelta
from django.conf import settings
import requests
from django.utils import timezone
from .models import WeatherData
from .serializers import WeatherDataSerializer


class WeatherDataViewSet(viewsets.ViewSet):
    def create(self, request):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        detailing_type = request.data.get("detailing_type")

        queryset = WeatherData.objects.filter(
            latitude=latitude,
            longitude=longitude,
            detailing_type=detailing_type,
            timestamp__gte=(
                timezone.now() - timedelta(minutes=settings.DATA_EXPIRY_MINUTES)
            ),
        )

        if queryset.exists():
            weather_data = queryset.first()
            serializer = WeatherDataSerializer(weather_data)
            return Response(serializer.data)

        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude={detailing_type}&appid={settings.WEATHER_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if detailing_type not in settings.DETAILING_TYPES:
                raise Exception(
                    f"Invalid detailing_type: {detailing_type}. Valid values are: {settings.DETAILING_TYPES}"
                )
            weather_data = WeatherData.objects.create(
                latitude=latitude,
                longitude=longitude,
                detailing_type=detailing_type,
                data=data,
            )
            serializer = WeatherDataSerializer(weather_data)
            return Response(serializer.data)
        else:
            raise Exception(
                f"Error fetching weather data. Status code: {response.status_code}"
            )

    def retrieve(self, request, pk=None):
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")
        detailing_type = request.GET.get("detailing_type")

        queryset = WeatherData.objects.filter(
            latitude=latitude,
            longitude=longitude,
            detailing_type=detailing_type,
            timestamp__gte=(
                timezone.now() - timedelta(minutes=settings.DATA_EXPIRY_MINUTES)
            ),
        )

        if queryset.exists():
            weather_data = queryset.first()
            serializer = WeatherDataSerializer(weather_data)
            return Response(serializer.data)
        else:
            url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude={detailing_type}&appid={settings.WEATHER_API_KEY}"

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if detailing_type not in settings.DETAILING_TYPES:
                    raise Exception(
                        f"Invalid detailing_type: {detailing_type}. Valid values are: {settings.DETAILING_TYPES}"
                    )
                weather_data = WeatherData.objects.create(
                    latitude=latitude,
                    longitude=longitude,
                    detailing_type=detailing_type,
                    data=data,
                )
                serializer = WeatherDataSerializer(weather_data)
                return Response(serializer.data)
            else:
                raise Exception(
                    f"Error fetching weather data. Status code: {response.status_code}"
                )

    def list(self, request):
        queryset = WeatherData.objects.all()
        serializer = WeatherDataSerializer(queryset, many=True)
        return Response(serializer.data)
