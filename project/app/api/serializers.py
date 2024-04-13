from rest_framework.serializers import HyperlinkedModelSerializer, SerializerMethodField
from ..models import Aliment

class AlimentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Aliment
        fields = "__all__"
