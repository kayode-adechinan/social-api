from common.permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from socialaccount import filters
from socialaccount.models import SocialAccount
from socialaccount.serializers import SocialAccountSerializer


class CanSetSocialAccount(APIException):
    status_code = 500
    default_detail = "Can set socialaccount"
    default_code = "can_set_socialaccount"


# Create your views here.
class SocialAccountViewSet(viewsets.ModelViewSet):
    queryset = SocialAccount.objects.all()
    serializer_class = SocialAccountSerializer
    # filterset_class = filters.SocialAccountFilter
    filter_fields = ["identifier", "user", "network", "updated_date"]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):

        # grab inputs
        inputs = serializer.validated_data
        # check if account not already exist
        existed_social_account = SocialAccount.objects.filter(
            user=self.request.user, network=inputs["network"]
        ).count()

        if existed_social_account > 0:
            raise CanSetSocialAccount()

        serializer.save(user=self.request.user)

    @action(detail=False)
    def me(self, request):
        my_accounts = SocialAccount.objects.filter(user=request.user)

        page = self.paginate_queryset(my_accounts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_accounts, many=True)
        return Response(serializer.data)
