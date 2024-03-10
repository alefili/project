from rest_framework.viewsets import ModelViewSet

from ..models import Aliment, Reteta

from .serializers import AlimentSerializer, RetetaSerializer

class AlimentViewSet(ModelViewSet):
    queryset = Aliment.objects.all()
    serializer_class = AlimentSerializer


class RetetaViewSet(ModelViewSet):
    queryset = Reteta.objects.all()
    serializer_class = RetetaSerializer
