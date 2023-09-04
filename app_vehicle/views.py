from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics

from app_vehicle.models import Car, Moto, Milage
from app_vehicle.serializers import CarSerializers, MotoSerializers, MilageSerializers, MotoMilageSerializers, \
    MotoCreateSerializers


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializers
    queryset = Car.objects.all()


class MotoCreateAPIView(generics.CreateAPIView):
    # serializer_class = MotoSerializers
    serializer_class = MotoCreateSerializers


class MotoListAPIView(generics.ListAPIView):
    serializer_class = MotoSerializers
    queryset = Moto.objects.all()


class MotoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MotoSerializers
    queryset = Moto.objects.all()


class MotoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MotoSerializers
    queryset = Moto.objects.all()


class MotoDestroyAPIView(generics.DestroyAPIView):
    queryset = Moto.objects.all()


class MilageCreateAPIView(generics.CreateAPIView):
    serializer_class = MilageSerializers


class MotoMilageListAPIView(generics.ListAPIView):
    queryset = Milage.objects.filter(moto__isnull=False)
    serializer_class = MotoMilageSerializers


# Фильтрация
class MilageListAPIView(generics.ListAPIView):
    serializer_class = MilageSerializers
    queryset = Milage.objects.all()
    # filter_backends = [DjangoFilterBackend] # Бэкенд для обработки фильтра без сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра с сортировкой
    filterset_fields = ('car', 'moto')  # Набор полей для фильтрации
    ordering_fields = ('year',)
