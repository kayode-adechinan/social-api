from rest_framework import viewsets
from rest_framework import viewsets
from like.models import Like
from like.serializers import LikeSerializer
from rest_framework import viewsets, permissions
from common.permissions import CanUnlike
from like.models import Like
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # filterset_class = filters.SocialAccountFilter
    filter_fields = ["likee", "liker", "updated_date"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CanUnlike]

    def perform_create(self, serializer):
        serializer.save(liker=self.request.user)

    @action(detail=False)
    def me(self, request):
        my_likers = Like.objects.filter(likee=request.user)

        page = self.paginate_queryset(my_likers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_likers, many=True)
        return Response(serializer.data)
