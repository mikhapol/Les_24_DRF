from django.shortcuts import render
from rest_framework import viewsets

from app_vehicle.models import Car
from app_vehicle.serializers import CarSerializers


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializers
    queryset = Car.objects.all()


