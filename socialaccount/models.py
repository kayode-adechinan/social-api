from django.db import models
from user.models import User
from network.models import Network

# Create your models here.
class SocialAccount(models.Model):
    identifier = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="socialaccounts", null=True
    )
    network = models.ForeignKey(
        Network, related_name="socialaccounts", on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_date",)
        unique_together = ("user", "network")

    def __str__(self):
        return self.identifier
