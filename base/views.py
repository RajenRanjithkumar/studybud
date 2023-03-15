from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q # to include or/and condition for queries 

from django.contrib.auth.models import User
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  #djangos default form

# Create your views here.


# rooms = [
#     {'id':1, 'name':"Lets Learn python!!"},
#     {'id':2, 'name':"Design"},
#     {'id':3, 'name':"with django"}
# ]


def loginPage(request):

    page = "login"


    if request.user.is_authenticated:
        return redirect('home')


    if request.method == "POST":

        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        

        if username != '' and password != '':
            try:
                user = User.objects.get(username = username)
            except:

                messages.error(request, " User does not exist ") #Django flash messages
        else:
            messages.error(request, " Username or password cannot be empty ") #Django flash messages

        

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, "Username or password does not exist")
            

    context ={"page":page}
    return render(request, "base/login_register.html", context)

def logoutUser(request):
    
    logout(request)

    return redirect('home')

def registerPage(request):

    #page = "register"

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        else:

            messages.error(request, "An error occured during registration")


    return render(request, "base/login_register.html", {'form':form})


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
    #room_messages = Message.objects.all()

    #Recent Activities
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))

    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages': room_messages}
    
    # passing the rooms dict to the html file
    return render(request, "base/home.html", context)                    

def room(request, pk):

    # get a specific object from Room DB
    room = Room.objects.get(id = pk)

    # query to get all the messages of a particular room
    # order_by('-')  to get the coverasations in descending order
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method =='POST':

        message = Message.objects.create(

            user = request.user,
            room = room,
            body = request.POST.get('body') # get the message from html form

        )

        #add messaging user to ROOm participants
        room.participants.add(request.user)

        return redirect('room', pk = room.id)


    context = {"room": room, 
               "room_messages": room_messages, 
               "participants":participants}

    return render(request, "base/room.html", context)


def userProfile(request, pk):

    user = User.objects.get(id=pk)

    rooms = user.room_set.all() # get all the user rooms 
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics':topics }

    return render(request, 'base/profile.html', context)


@login_required(login_url='login')  #decorater to force a user to login before logging in
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

    
    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    # update DB
    if request.method == 'POST':

        form = RoomForm(request.POST, instance=room) # instance=room will update the value of that paticular room
                                                     # else it will create a new entry

        if form.is_valid():
            form.save()
            return redirect("home")


    context = {'form': form}
    return render(request, "base/room_form.html", context)

## later added
@login_required(login_url='login') 
def deleteRoom(request, pk):

    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':

        room.delete()

        return redirect("home")

    return render(request, "base/delete.html", {'obj':room})


@login_required(login_url='login') 
def deleteMessage(request, pk):

    message = Message.objects.get(id = pk)
    room = message.room

    if request.user != message.user:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':

        message.delete()

        return redirect('room', pk = room.id)
        #return redirect("home")

    return render(request, "base/delete.html", {'obj':message})


