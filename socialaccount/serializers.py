from rest_framework import serializers
from socialaccount import models
from user.serializers import UserSerializer


class SocialAccountSerializer(serializers.ModelSerializer):
    networkInfo = serializers.SerializerMethodField(method_name="calculate_networkInfo")
    networkInfoLogo = serializers.SerializerMethodField(
        method_name="calculate_networkInfoLogo"
    )
    userInfo = serializers.SerializerMethodField(method_name="calculate_userInfo")

    class Meta:
        fields = (
            "id",
            "network",
            "identifier",
            "created_date",
            "updated_date",
            "networkInfo",
            "networkInfoLogo",
            "userInfo",
        )
        model = models.SocialAccount

    def calculate_networkInfo(self, instance):
        return instance.network.platform

    def calculate_networkInfoLogo(self, instance):
        return instance.network.logo

    def calculate_userInfo(self, instance):
        request = self.context.get("request")
        if instance.user == request.user:
            return "It's you"
        return UserSerializer(instance.user).data
