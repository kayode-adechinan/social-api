from django.db import models
from relationship.models import Relationship

# Create your models here.
class Notification(models.Model):
    isReceived = models.BooleanField(default=False)
    message = models.CharField(max_length=150, null=True, blank=True)
    relationship = models.ForeignKey(
        Relationship,
        related_name="notifications",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_date",)

    def __str__(self):
        return str(self.isReceived)
