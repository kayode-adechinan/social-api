from common.permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from socialaccount.serializers import SocialAccountSerializer
from user.models import User

from contact.models import Contact
from contact.serializers import ContactSerializer


# Create your views here.
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    # filterset_class = filters.SocialAccountFilter
    filter_fields = ["user", "socialaccount", "updated_date"]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # def perform_create(self, serializer):
    # serializer.save(user=self.request.user)

    @action(detail=False)
    def me(self, request):
        my_contacts = Contact.objects.filter(user=request.user)

        friends_ids = []

        for contact in my_contacts:
            friends_ids.append(contact.socialaccount.user.id)

        friends_ids_uniques = list(dict.fromkeys(friends_ids))

        friends_infos = User.objects.filter(pk__in=friends_ids_uniques)

        # Get all my contacts

        # Create grouped data
        grouped_data = []

        for friend in friends_infos:
            grouped_data.append(
                {
                    "id": "",
                    "socialaccount": "",
                    "user": friend.id,
                    "user_firstname": friend.first_name,
                    "user_lastname": friend.last_name,
                    "user_avatar": friend.avatar,
                    "user_profession": friend.profession,
                    "user_birthday": friend.birthday,
                    "user_city": friend.city,
                    "user_phone": friend.phone,
                    "user_bio": friend.bio,
                    "networks": [],
                }
            )

        for gd in grouped_data:
            contacts_info = Contact.objects.filter(
                user=request.user, socialaccount__user__pk=gd["user"]
            )
            entries = []
            for ci in contacts_info:
                entry = {
                    "identifier": ci.socialaccount.identifier,
                    "network": ci.socialaccount.network.id,
                    "networkInfo": ci.socialaccount.network.platform,
                }
                entries.append(entry)
            gd["networks"] = entries

        page = self.paginate_queryset(my_contacts)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
            return Response({"results": grouped_data})
            # return Response({"results": cleaned})

        serializer = self.get_serializer(my_contacts, many=True)
        # return Response(serializer.data)
        return Response({"results": grouped_data})
        # return Response({"results": cleaned})
