# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from notification.serializers import NotificationSerializer
from rest_framework import viewsets
from notification.models import Notification
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_fields = ["isReceived", "relationship", "updated_date"]
    # filterset_class = ItemFilter
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    # serializer.save(user=self.request.user)

    @action(detail=False)
    def me(self, request):

        my_notifications = Notification.objects.filter(
            relationship__receiver=request.user,
            relationship__isReacted=False,
            isReceived=False,
        )

        type = request.query_params.get("type", None)
        if type is not None:
            print("youre in")
            if type == "reacted":
                print(request.user.id)
                my_notifications = Notification.objects.filter(
                    relationship__sender=request.user,
                    relationship__isReacted=True,
                    message="REACTION",
                    isReceived=False,
                )
            if type == "accepted":
                my_notifications = Notification.objects.filter(
                    relationship__sender=request.user,
                    relationship__isAccepted=True,
                    message="ACCEPTANCE",
                    isReceived=False,
                )
            if type == "rejected":
                my_notifications = Notification.objects.filter(
                    relationship__sender=request.user,
                    relationship__isAccepted=False,
                    message="REJECTION",
                    isReceived=False,
                )

        page = self.paginate_queryset(my_notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_notifications, many=True)
        return Response(serializer.data)
