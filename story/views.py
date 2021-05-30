from rest_framework import viewsets
from story.serializers import StorySerializer
from rest_framework import viewsets
from story.models import Story
from common.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    # filterset_class = filters.SocialAccountFilter
    filter_fields = ["text", "media", "user", "updated_date"]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    """
    def get_queryset(self):
        
        if self.action == "destroy":
            return Story.objects.all()
        if self.action == "retrieve":
            return Story.objects.all()
        queryset = Story.objects.exclude(user=self.request.user)
        return queryset
    """

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False)
    def me(self, request):
        my_stories = Story.objects.filter(user=request.user)

        page = self.paginate_queryset(my_stories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_stories, many=True)
        return Response(serializer.data)
