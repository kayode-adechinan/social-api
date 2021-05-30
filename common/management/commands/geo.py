from django.core.management.base import BaseCommand
import json
from django.contrib.gis.geos import fromstr
from pathlib import Path
from network.models import Network
from user.models import User

import random

geodata = [
    {
        "longitude": "-80.1958809",
        "latitude": "25.8478742",
    },
    {
        "longitude": "-80.1888305",
        "latitude": "25.7741593",
    },
    {
        "latitude": "25.7853013",
        "longitude": "-80.1740071",
    },
    {
        "latitude": "25.7753719",
        "longitude": "-80.188012",
    },
    {
        "latitude": "25.8327549",
        "longitude": "-80.1871658",
    },
    {
        "latitude": "25.7639185",
        "longitude": "-80.2854811",
    },
    {
        "latitude": "25.7286438",
        "longitude": "-80.2420384",
    },
    {
        "latitude": "25.7901905",
        "longitude": "-80.1857491",
    },
    {
        "latitude": "25.8101674",
        "longitude": "-80.1940194",
    },
    {
        "latitude": "25.7744306",
        "longitude": "-80.1888075",
    },
]


from faker import Faker

fake = Faker()

users = User.objects.all()

Faker.seed(0)


def set_geo():
    for u in users:
        coord = fake.local_latlng()
        u.longitude = str(coord[1])
        u.latitude = str(coord[0])
        u.save()


def set_geo_2():
    for u in users:
        coord = random.choice(geodata)
        u.longitude = str(coord["longitude"])
        u.latitude = str(coord["latitude"])
        u.location = fromstr("POINT(%s %s)" % (coord["longitude"], coord["latitude"]))
        u.save()


class Command(BaseCommand):
    help = "fake data generator"

    def handle(self, *args, **options):
        set_geo_2()
        self.stdout.write(self.style.SUCCESS("done!"))
