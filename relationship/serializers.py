from rest_framework import serializers
from relationship import models


class RelationshipSerializer(serializers.ModelSerializer):


    class Meta:
        fields = (
            "id",
            "receiver",
            "message",
            "socialaccount",
            "isReacted",
            "isAccepted",
            "created_date",
            "updated_date",
        )
        model = models.Relationship

    
  