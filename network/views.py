from django.shortcuts import render
from rest_framework import viewsets
from network.serializers import NetworkSerializer
from rest_framework import viewsets
from network.models import Network


# Create your views here.
class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_fields = ['platform', 'updated_date']
    #filterset_class = ItemFilter
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly ]

    #def perform_create(self, serializer):
        #serializer.save(user=self.request.user)
