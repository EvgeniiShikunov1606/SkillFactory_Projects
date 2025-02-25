from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Stopover
from .serializers import StopoverSerializer


class StopoverViewSet(viewsets.ModelViewSet):
    queryset = Stopover.objects.all()
    serializer_class = StopoverSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email']

