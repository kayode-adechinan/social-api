# Create your models here.
# from django.db import models
from django.contrib.gis.db import models


# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import fromstr


class User(AbstractUser):
    phone = models.CharField(max_length=30, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)
    profession = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    location = models.PointField(null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        if self.longitude and self.latitude:
            self.location = fromstr("POINT(%s %s)" % (self.longitude, self.latitude))
        super().save(*args, **kwargs)
