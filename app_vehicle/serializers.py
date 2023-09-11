from rest_framework import serializers
from app_vehicle.models import Car, Moto, Milage
from app_vehicle.validators import TitleValidator


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
    # milage = MilageSerializers(source='milage_set', many=True)
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
    # last_milage = serializers.IntegerField(source='milage_set.all.first.milage')
    last_milage = serializers.IntegerField(source='milage.all.first.milage', read_only=True)

    class Meta:
        model = Moto
        fields = '__all__'


class MotoMilageSerializers(serializers.ModelSerializer):
    moto = MotoSerializers()

    class Meta:
        model = Milage
        # fields = '__all__'
        fields = ('milage', 'moto', 'year',)


class MotoCreateSerializers(serializers.ModelSerializer):
    milage = MilageSerializers(many=True)

    class Meta:
        model = Moto
        fields = '__all__'
        validators = [
            TitleValidator(field='title'),
            serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Moto.objects.all())
        ]

    def create(self, validated_data):
        milage = validated_data.pop('milage')

        moto_item = Moto.objects.create(**validated_data)

        for a in milage:
            Milage.objects.create(**a, moto=moto_item)

        return moto_item
