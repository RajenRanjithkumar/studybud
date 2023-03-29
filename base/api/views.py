from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer



# check out https://www.django-rest-framework.org/tutorial/2-requests-and-responses/ for docs



@api_view(['GET'])   #['GET', 'POST', 'PUT']
def getRoutes(request):

    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id']


    return Response(routes) #safe parameter converts the routes list into Json data


#get all the rooms
@api_view(['GET'])
def getRooms(request):

    rooms = Room.objects.all()

    # serializers has to created to convert the backend python objs to json objs
     # many = true for list of objs and many=false for one objs
    serializer = RoomSerializer(rooms, many=True) 

    return Response(serializer.data)

#get a specific the room
@api_view(['GET'])
def getRoom(request, pk):

    room = Room.objects.get(id=pk)

    # serializers has to created to convert the backend python objs to json objs
     # many = true for list of objs and many=false for one objs
    serializer = RoomSerializer(room, many=False) 

    return Response(serializer.data)