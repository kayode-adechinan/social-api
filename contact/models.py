import socialaccount
from django.db import models
from socialaccount.models import SocialAccount
from user.models import User


# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contacts", null=True
    )
    socialaccount = models.ForeignKey(
        SocialAccount, related_name="socialaccounts", on_delete=models.DO_NOTHING
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_date",)
        unique_together = ("user", "socialaccount")

    def __str__(self):
        return str(self.created_date)

        # user, socialaccount,
