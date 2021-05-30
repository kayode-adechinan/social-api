from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass
