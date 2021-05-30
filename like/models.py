from django.db import models
from user.models import User

# Create your models here.
class Like(models.Model):
    likee = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="likers", null=True
    )
    liker = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="likees", null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_date",)
        unique_together = ("likee", "liker")

    def __str__(self):
        return str(self.likee) + str(self.liker)
