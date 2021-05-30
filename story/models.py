import socialaccount
from django.db import models
from user.models import User

# Create your models here.
class Story(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stories", null=True
    )
    text = models.TextField(null=True)
    media = models.URLField(null=True)
    isVideo = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_date",)

    def __str__(self):
        return self.text
