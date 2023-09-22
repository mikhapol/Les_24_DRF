# Generated by Django 4.2.4 on 2023-09-22 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_vehicle', '0008_alter_milage_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='moto',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
