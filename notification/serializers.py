import relationship
from rest_framework import serializers
from notification import models
from user.serializers import UserSerializer
from relationship.serializers import RelationshipSerializer


class NotificationSerializer(serializers.ModelSerializer):

    relationshipInfo = serializers.SerializerMethodField(
        method_name="calculate_relationshipInfo"
    )

    class Meta:
        fields = (
            "id",
            "isReceived",
            "relationship",
            "message",
            "created_date",
            "updated_date",
            "relationshipInfo",
        )
        model = models.Notification

    def calculate_relationshipInfo(self, instance):

        sender = UserSerializer(instance.relationship.sender).data
        receiver = UserSerializer(instance.relationship.receiver).data
        relationship = RelationshipSerializer(instance.relationship).data

        response = {
            "sender": sender,
            "receiver": receiver,
            "relationship": relationship,
        }

        return response
