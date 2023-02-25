from django.forms import ModelForm
from .models import Room


# class based form that will be created automatically by django wrt Data class
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' # this will create all the input fields with wrt to our ROOM data class