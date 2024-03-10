from rest_framework.serializers import HyperlinkedModelSerializer, SerializerMethodField
from ..models import Reteta, Aliment

class RetetaSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Reteta
        fields = "__all__"

class AlimentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Aliment
        fields = "__all__"
