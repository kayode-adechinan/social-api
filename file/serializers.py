from rest_framework import serializers
from file import models


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "file",
            "url",
            "created_date",
            "updated_date",
        )
        extra_kwargs = {"file": {"write_only": True}, "url": {"read_only": True}}
        model = models.File
