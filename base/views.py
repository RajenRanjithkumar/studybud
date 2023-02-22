from django.shortcuts import render
from .models import Room

# Create your views here.


# rooms = [
#     {'id':1, 'name':"Lets Learn python!!"},
#     {'id':2, 'name':"Design"},
#     {'id':3, 'name':"with django"}
# ]


def home(request):
    
    # the gets all the objects
    rooms = Room.objects.all()

    context = {'rooms': rooms}

    return render(request, "base/home.html", context) # passing the rooms dict to the html file

def room(request, pk):

    # get a specific object from Room DB
    room = Room.objects.get(id = pk)

    context = {"room": room}

    return render(request, "base/room.html", context)