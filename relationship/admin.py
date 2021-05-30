from django.contrib import admin

# Register your models here.
from .models import Relationship


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    pass
