from django.db import models
from socialaccount.models import SocialAccount
from user.models import User


# Create your models here.
class Relationship(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="receivers", null=True
    )
    receiver = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="senders", null=True
    )
    socialaccount = models.ForeignKey(
        SocialAccount,
        on_delete=models.DO_NOTHING,
        related_name="relationships",
        null=True,
        blank=True,
    )
    message = models.TextField(null=True, default=False)
    isReacted = models.BooleanField(null=True, default=False)
    isAccepted = models.BooleanField(null=True, default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_date",)
        unique_together = ("sender", "receiver", "socialaccount")




    def __str__(self):
        return str(self.isAccepted)
