from rest_framework import serializers
from story import models
from user.serializers import UserSerializer


class StorySerializer(serializers.ModelSerializer):
    userInfo = serializers.SerializerMethodField(method_name="calculate_userInfo")

    class Meta:
        fields = (
            "id",
            "text",
            "media",
            "isVideo",
            "created_date",
            "updated_date",
            "userInfo",
        )
        model = models.Story

    def calculate_userInfo(self, instance):
        request = self.context.get("request")
        # if instance.user == request.user:
        # return "In Your Localstorage"
        return UserSerializer(instance.user).data
