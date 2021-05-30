from rest_framework import serializers
from like import models
from user.serializers import UserSerializer


class LikeSerializer(serializers.ModelSerializer):

    likeeInfo = serializers.SerializerMethodField(method_name="calculate_likeeInfo")
    likerInfo = serializers.SerializerMethodField(method_name="calculate_likerInfo")

    class Meta:
        fields = (
            "id",
            "likee",
            "likeeInfo",
            "liker",
            "likerInfo",
            "created_date",
            "updated_date",
        )
        extra_kwargs = {
            "liker": {"read_only": True},
        }
        model = models.Like

    def calculate_likeeInfo(self, instance):
        return UserSerializer(instance.likee).data

    def calculate_likerInfo(self, instance):
        return UserSerializer(instance.liker).data
