from rest_framework.serializers import ModelSerializer
from base.models import Room


# serializers has to created to convert the backend python objs to json objs
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'