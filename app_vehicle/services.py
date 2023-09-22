import json
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import status


def convert_currencies(rub_price):
    usd_price = 0
    response = requests.get(
        f'{settings.CUR_API_URL}v3/latest?apikey={settings.CUR_API_KEY}&currencies=RUB'
    )
    if response.status_code == status.HTTP_200_OK:
        # print(response.json())
        usd_rate = response.json()['data']['RUB']['value']
        # print(usd_rate)
        usd_price = rub_price * usd_rate

    # print(response)
    # usd_price = rub_price *90

    return usd_price


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.HOURS,
    )
    PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        name='Importing contacts',  # simply describes this periodic task.
        task='proj.tasks.import_contacts',  # name of task.
        args=json.dumps(['arg1', 'arg2']),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
    )
