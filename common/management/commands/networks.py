from django.core.management.base import BaseCommand
import json
from django.contrib.gis.geos import fromstr
from pathlib import Path
from network.models import Network


def load_networks():
    Network.objects.create(platform="facebook")
    Network.objects.create(platform="instagram")
    Network.objects.create(platform="whatsapp")
    Network.objects.create(platform="telegram")
    Network.objects.create(platform="youtube")
    Network.objects.create(platform="snapchat")
    Network.objects.create(platform="twitter")
    Network.objects.create(platform="linkedin")
    Network.objects.create(platform="tiktok")


class Command(BaseCommand):
    help = "fake data generator"

    def handle(self, *args, **options):

        load_networks()
        self.stdout.write(self.style.SUCCESS("done!"))
