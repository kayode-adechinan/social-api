from django.shortcuts import render
from rest_framework import viewsets
from file.serializers import FileSerializer
from rest_framework import viewsets
from file.models import File


# Create your views here.
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    #filter_fields = ['platform', 'updated_date']
    #filterset_class = ItemFilter
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly ]

    #def perform_create(self, serializer):
        #serializer.save(user=self.request.user)
