from rest_framework import serializers
from socialaccount import models


class NetworkSerializer(serializers.ModelSerializer):
    networkInfo = serializers.SerializerMethodField(method_name="calculate_networkInfo")

    class Meta:
        fields = (
            "id",
            "network",
            "identifier",
            "created_date",
            "updated_date",
            "networkInfo",
        )
        model = models.SocialAccount

    def calculate_networkInfo(self, instance):
        return instance.network.platform