from django.shortcuts import render, redirect

from django.db.models import Q # to include or/and condition for queries 

#from django.contrib.auth.models import User
# importing our own user model
from .models import Room, Topic, Message, User

from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm  #djangos default form


from .forms import RoomForm, UserForm, MyUserCreationForm

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

        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        

        if email != '' and password != '':
            try:
                user = User.objects.get(email = email)
            except:

                messages.error(request, " User does not exist ") #Django flash messages
        else:
            messages.error(request, " Username or password cannot be empty ") #Django flash messages

        

        user = authenticate(request, email=email, password=password)

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

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
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

    topics = Topic.objects.all()[0:5]#get the first 5 topics

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

    #get the message from front end
    if request.method =='POST':

        message = Message.objects.create(

            user = request.user,
            room = room,
            body = request.POST.get('body') # get the message from html form

        )

        #add messaging user to Room participants
        room.participants.add(request.user)

        return redirect('room', pk = room.id)


    context = {"room": room, 
               "room_messages": room_messages, 
               "participants":participants}

    return render(request, "base/room.html", context)


def userProfile(request, pk):

    user = User.objects.get(id=pk)
    # get all the user rooms 
    rooms = user.room_set.all() 
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics':topics }

    return render(request, 'base/profile.html', context)


@login_required(login_url='login')  #decorater to force a user to login before logging in
def createRoom(request):

    form = RoomForm()

    topics = Topic.objects.all()

    # get the data from the user
    if request.method == 'POST':


        topic_name = request.POST.get('topic')

        # get_or_create():
        #     if the topic is already available in db 
        #         it assigns to topic
        #     else 
        #         it assigns to created

        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(

            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),

        )

        #will process all the input data 
        # form = RoomForm(request.POST)
        # if form.is_valid():

        #     # to make the logged in user as the host
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()

            #will save the data in the db
            #form.save()

            #send the user to the home page
        return redirect("home")

    context = {"form": form, 'topics': topics}
    return render(request, "base/room_form.html", context)



# pk primary key
@login_required(login_url='login')
def updateRoom(request, pk):

    room = Room.objects.get(id = pk)
    # instance=room will pre fill the form with the existing contents
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    
    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    # update DB
    if request.method == 'POST':


        topic_name = request.POST.get('topic')

        # get_or_create():
        #     if the topic is already available in db 
        #         it assigns to topic
        #     else 
        #         it assigns to created

        topic, created = Topic.objects.get_or_create(name = topic_name)

        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()

        # form = RoomForm(request.POST, instance=room) # instance=room will update the value of that paticular room
        #                                              # else it will create a new entry

        # if form.is_valid():
        #     form.save()
        return redirect("home")


    context = {'form': form, 'topics': topics, 'room':room}
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

@login_required(login_url='login')
def updateUser(request):

    user = request.user
    form = UserForm(instance=user)

    context = {'form':form}

    if request.method == 'POST':

        form = UserForm(request.POST, request.FILES,instance=user) #request.FILES to get the image

        if form.is_valid():
            form.save()

            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update_user.html', context)


def topicsPage(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''    # '' will fetch the entire dataset 
    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'base/topics.html', {'topics':topics})

def activityPage(request):

    room_messages = Message.objects.all()

    return render(request, 'base/activity.html', {'room_messages':room_messages})


