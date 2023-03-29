from django.forms import ModelForm

#from django.contrib.auth.models import User
# importing our own user model
from .models import Room, User




# class based form that will be created automatically by django wrt Data class
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' # this will render all the input fields with wrt to our ROOM data class
        exclude = ['host','participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
