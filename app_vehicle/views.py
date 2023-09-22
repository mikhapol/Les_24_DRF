from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from app_vehicle.models import Car, Moto, Milage
from app_vehicle.paginators import VehiclePaginator
from app_vehicle.permission import IsOwnerOrStaff
from app_vehicle.serializers import CarSerializers, MotoSerializers, MilageSerializers, MotoMilageSerializers, \
    MotoCreateSerializers
from app_vehicle.tasks import check_milage


class CarViewSet(viewsets.ModelViewSet):
    """Машины CarViewSet"""
    serializer_class = CarSerializers
    queryset = Car.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]


class MotoCreateAPIView(generics.CreateAPIView):
    """Мотоциклы создание"""
    # serializer_class = MotoSerializers
    serializer_class = MotoCreateSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_moto = serializer.save()
        new_moto.owner = self.request.user
        new_moto.save()


class MotoListAPIView(generics.ListAPIView):
    """Мотоциклы просмотр"""
    serializer_class = MotoSerializers
    queryset = Moto.objects.all()
    pagination_class = VehiclePaginator


class MotoRetrieveAPIView(generics.RetrieveAPIView):
    """Мотоциклы просмотр по ID"""
    serializer_class = MotoSerializers
    queryset = Moto.objects.all()


class MotoUpdateAPIView(generics.UpdateAPIView):
    """Мотоциклы редактирование"""
    serializer_class = MotoSerializers
    queryset = Moto.objects.all()
    permission_classes = [IsOwnerOrStaff]


class MotoDestroyAPIView(generics.DestroyAPIView):
    """Мотоциклы удаление"""
    queryset = Moto.objects.all()


class MilageCreateAPIView(generics.CreateAPIView):
    """Пробег создание"""
    serializer_class = MilageSerializers

    def perform_create(self, serializer):
        new_milage = serializer.save()
        if new_milage.car:
            check_milage.delay(new_milage.car_id, 'Car')
        else:
            check_milage.delay(new_milage.moto_id, 'Moto')


class MotoMilageListAPIView(generics.ListAPIView):
    """Просмотр пробега в мотоциклах"""
    queryset = Milage.objects.filter(moto__isnull=False)
    serializer_class = MotoMilageSerializers


# Фильтрация
class MilageListAPIView(generics.ListAPIView):
    """Просмотр всех пробегов"""
    serializer_class = MilageSerializers
    queryset = Milage.objects.all()
    # filter_backends = [DjangoFilterBackend] # Бэкенд для обработки фильтра без сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра с сортировкой
    filterset_fields = ('car', 'moto')  # Набор полей для фильтрации
    ordering_fields = ('year',)
