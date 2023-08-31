from django.urls import path

from app_vehicle.apps import AppVehicleConfig
from rest_framework.routers import DefaultRouter

from app_vehicle.views import CarViewSet, MotoCreateAPIView, MotoListAPIView, MotoRetrieveAPIView, MotoUpdateAPIView, \
    MotoDestroyAPIView

app_name = AppVehicleConfig.name

router = DefaultRouter()
router.register('cars', CarViewSet, basename='cars')

urlpatterns = [
    path('moto/create/', MotoCreateAPIView.as_view(), name='moto-create'),
    path('moto/', MotoListAPIView.as_view(), name='moto-list'),
    path('moto/<int:pk>/', MotoRetrieveAPIView.as_view(), name='moto-get'),
    path('moto/update/<int:pk>/', MotoUpdateAPIView.as_view(), name='moto-update'),
    path('moto/delete/<int:pk>/', MotoDestroyAPIView.as_view(), name='moto-delete'),

] + router.urls
