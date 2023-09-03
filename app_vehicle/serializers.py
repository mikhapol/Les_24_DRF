from rest_framework import serializers
from app_vehicle.models import Car, Moto, Milage


class MilageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Milage
        fields = '__all__'


class CarSerializers(serializers.ModelSerializer):
    # Практика. Кастомизация сериализаторов

    # Первый подход
    # last_milage = serializers.IntegerField(source='milage_set.all.first.milage')
    # Второй подход
    last_milage = serializers.SerializerMethodField()
    milage = MilageSerializers(source='milage_set', many=True)

    class Meta:
        model = Car
        fields = '__all__'

    # Добавление ко второму методу
    def get_last_milage(self, instance):
        if instance.milage_set.all().first():
            return instance.milage_set.all().first().milage
        return 0
    # Или
    # @staticmethod
    # def get_last_milage(instance):
    #     if instance.milage_set.all().first():
    #         return instance.milage_set.all().first().milage
    #     return 0


class MotoSerializers(serializers.ModelSerializer):
    last_milage = serializers.IntegerField(source='milage_set.all.first.milage')

    class Meta:
        model = Moto
        fields = '__all__'


class MotoMilageSerializers(serializers.ModelSerializer):
    moto = MotoSerializers()
    class Meta:
        model = Milage
        # fields = '__all__'
        fields = ('milage', 'moto', 'year',)
