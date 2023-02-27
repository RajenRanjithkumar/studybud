from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q # to include or/and condition for queries 

from django.contrib.auth.models import User
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout

# Create your views here.


# rooms = [
#     {'id':1, 'name':"Lets Learn python!!"},
#     {'id':2, 'name':"Design"},
#     {'id':3, 'name':"with django"}
# ]


def loginPage(request):


    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:

            user = User.objects.get(username = username)

        except:

            messages.error(request, " User does not exist ") #Django flash messages

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, "Username or password does not exist")
            

    context ={}
    return render(request, "base/login_register.html", context)

def logoutUser(request):
    logout(request)

    return redirect('home')



def home(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''    # '' will fetch the entire dataset 
    # the gets all the objects
    
     #topic__name__icontains is the query i in icontains represents case sensitive
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |  # syntax for contains querry
        Q(name__icontains = q) |
        Q(description__icontains = q)
        
        )            

    topics = Topic.objects.all()

    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count}

    return render(request, "base/home.html", context)                    # passing the rooms dict to the html file

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

