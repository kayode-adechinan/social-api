from django.contrib import admin

# Register your models here.
from .models import Network


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    pass