from common.permissions import CanEditRelation, IsOwnerOrReadOnly
from contact.models import Contact
from django.shortcuts import render
from notification.models import Notification
from rest_framework import permissions, viewsets
from rest_framework.exceptions import APIException
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from socialaccount.models import SocialAccount

from relationship.models import Relationship
from relationship.serializers import RelationshipSerializer


class CanEstablishRelationship(APIException):
    status_code = 500
    default_detail = "Can establish relationship"
    default_code = "can_establish_relationship"


# Create your views here.
class RelationshipViewSet(viewsets.ModelViewSet, UpdateModelMixin):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    # filterset_class = filters.SocialAccountFilter
    filter_fields = ["sender", "receiver", "isReacted", "isAccepted", "updated_date"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CanEditRelation]

    def perform_create(self, serializer):

        # grad the data
        inputs = serializer.validated_data
        print("data:")
        print(inputs["socialaccount"].id)
        # check if the sender and the receiver are not the same person
        if self.request.user == inputs["receiver"]:
            raise CanEstablishRelationship()

        # check if the relationship is not already there:
        existed_contacts = Contact.objects.filter(
            user__pk=self.request.user.id,
            socialaccount__user__pk=inputs["receiver"].id,
            socialaccount__network__pk=inputs["socialaccount"].id,
        ).count()

        if existed_contacts > 0:
            raise CanEstablishRelationship()

        # check if the receiver did not already get the asking:
        # filter relation by sender, receiver and is reacted/isaccepted false
        existed_relationships = Relationship.objects.filter(
            sender__pk=self.request.user.id, receiver__pk=inputs["receiver"].id, isAccepted=False
        ).count()

        if existed_relationships > 0:
            raise CanEstablishRelationship()

        # create notification
        relationship = serializer.save(sender=self.request.user)

        Notification.objects.create(relationship=relationship, message="RECEPTION")

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.isReacted == True and instance.isAccepted == False:
            Notification.objects.create(relationship=instance, message="REACTION")
            return

        if instance.isAccepted == True:
            Notification.objects.create(relationship=instance, message="ACCEPTANCE")
            # Create contact
            # get socialaccount
            socialaccount = SocialAccount.objects.get(pk=instance.socialaccount.id)
            # user, socialaccount,
            Contact.objects.create(user=instance.sender, socialaccount=socialaccount)
            return

        if instance.isAccepted == False:
            Notification.objects.create(relationship=instance, message="REJECTION")
            return
