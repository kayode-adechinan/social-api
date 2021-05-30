from django.db import models

# Create your models here.
class Network(models.Model):
    platform = models.CharField(max_length=200, null=True, blank=True)
    logo = models.URLField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_date",)

    def __str__(self):
        return self.platform
