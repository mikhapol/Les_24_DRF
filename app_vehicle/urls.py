from app_vehicle.apps import AppVehicleConfig
from rest_framework.routers import DefaultRouter

from app_vehicle.views import CarViewSet

app_name = AppVehicleConfig.name

router = DefaultRouter()
router.register('cars', CarViewSet, basename='cars')

urlpatterns = [

] + router.urls
