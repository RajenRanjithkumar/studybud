from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

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


def createRoom(request):

    form = RoomForm()

    # get the data from the user
    if request.method == 'POST':

        #will process all the input data 
        form = RoomForm(request.POST)
        if form.is_valid():

            #will save the data in the db
            form.save()

            #send the user to the home page
            return redirect("home")



    context = {"form": form}
    return render(request, "base/room_form.html", context)

# pk primary key
def updateRoom(request, pk):

    room = Room.objects.get(id = pk)

    # instance=room will pre fill the form with the existing contents
    form = RoomForm(instance=room)
   
    # update DB
    if request.method == 'POST':

        form = RoomForm(request.POST, instance=room) # instance=room will update the value of that paticular room
                                                     # else it will create a new entry

        if form.is_valid():
            form.save()
            return redirect("home")


    context = {'form': form}
    return render(request, "base/room_form.html", context)

def deleteRoom(request, pk):

    room = Room.objects.get(id = pk)

    if request.method == 'POST':

        room.delete()

        return redirect("home")


    return render(request, "base/delete.html", {'obj':room})

