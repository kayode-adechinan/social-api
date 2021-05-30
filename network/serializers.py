from rest_framework import serializers
from network import models


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "platform",
            "logo",
            "created_date",
            "updated_date",
        )
        model = models.Network
