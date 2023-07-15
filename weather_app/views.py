# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import WeatherData
# from .serializers import WeatherDataSerializer
# from datetime import timedelta
# from django.conf import settings
# import requests
# from django.utils import timezone


# class WeatherForecastView(APIView):
#     def post(self, request):
#         latitude = request.data.get("latitude")
#         longitude = request.data.get("lon")
#         detailing_type = request.data.get("detailing_type")

#         try:
#             weather_data = WeatherData.objects.get(
#                 latitude=latitude,
#                 longitude=longitude,
#                 detailing_type=detailing_type,
#                 timestamp__gte=(
#                     timezone.now() - timedelta(minutes=settings.DATA_EXPIRY_MINUTES)
#                 ),
#             )
#             serializer = WeatherDataSerializer(weather_data)
#             return Response(serializer.data)
#         except WeatherData.DoesNotExist:
#             url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude={detailing_type}&appid={settings.WEATHER_API_KEY}"
#             print(url, "gggggggggggggggggggggggg")

#             response = requests.get(url)
#             if response.status_code == 200:
#                 data = response.json()
#                 if detailing_type not in settings.DETAILING_TYPES:
#                     raise Exception(
#                         f"Invalid detailing_type: {detailing_type}. Valid values are: {settings.DETAILING_TYPES}"
#                     )
#                 weather_data = WeatherData.objects.create(
#                     latitude=latitude,
#                     longitude=longitude,
#                     detailing_type=detailing_type,
#                     data=data,
#                 )
#                 serializer = WeatherDataSerializer(weather_data)
#                 return Response(serializer.data)
#             else:
#                 raise Exception(
#                     f"Error fetching weather data. Status code: {response.status_code}"
#                 )

#     def get(self, request):
#         latitude = request.GET.get("lat")
#         longitude = request.GET.get("lon")
#         detailing_type = request.GET.get("detailing_type")

#         try:
#             weather_data = WeatherData.objects.get(
#                 latitude=latitude,
#                 longitude=longitude,
#                 detailing_type=detailing_type,
#                 timestamp__gte=(
#                     timezone.now() - timedelta(minutes=settings.DATA_EXPIRY_MINUTES)
#                 ),
#             )
#             serializer = WeatherDataSerializer(weather_data)
#             return Response(serializer.data)
#         except WeatherData.DoesNotExist:
#             url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude={detailing_type}&appid={settings.WEATHER_API_KEY}"

#             response = requests.get(url)
#             if response.status_code == 200:
#                 data = response.json()
#                 if detailing_type not in settings.DETAILING_TYPES:
#                     raise Exception(
#                         f"Invalid detailing_type: {detailing_type}. Valid values are: {settings.DETAILING_TYPES}"
#                     )
#                 weather_data = WeatherData.objects.create(
#                     latitude=latitude,
#                     longitude=longitude,
#                     detailing_type=detailing_type,
#                     data=data,
#                 )
#                 serializer = WeatherDataSerializer(weather_data)
#                 return Response(serializer.data)
#             else:
#                 raise Exception(
#                     f"Error fetching weather data. Status code: {response.status_code}"
#                 )
