from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    pass
