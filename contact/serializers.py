from socialaccount.models import SocialAccount
from rest_framework import serializers
from contact import models
from rest_framework.response import Response
from user.serializers import UserSerializer


class ContactSerializer(serializers.ModelSerializer):
    socialAccountInfo = serializers.SerializerMethodField(
        method_name="calculate_socialaccountinfo"
    )

    class Meta:
        fields = (
            "id",
            "socialaccount",
            "user",
            "created_date",
            "updated_date",
            "socialAccountInfo",
        )
        model = models.Contact

    def calculate_socialaccountinfo(self, instance):
        request = self.context.get("request")
        if instance.socialaccount.user == request.user:
            return "It's you"
        response = {
            "contactInfo": UserSerializer(instance.socialaccount.user).data,
            "contactSocialAccountInfo": {
                "identifier": instance.socialaccount.identifier,
                "network": instance.socialaccount.network.platform,
            },
        }
        return response
