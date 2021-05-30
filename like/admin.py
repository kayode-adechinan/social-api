from django.contrib import admin

# Register your models here.
from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass