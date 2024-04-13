from rest_framework.viewsets import ModelViewSet

from ..models import Aliment

from .serializers import AlimentSerializer

class AlimentViewSet(ModelViewSet):
    queryset = Aliment.objects.all()
    serializer_class = AlimentSerializer

