from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass
