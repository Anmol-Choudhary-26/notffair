from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from user.models import Users
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import  generics, status
from Utils.helper_response import InvalidUserIdResponse
from .serializers import ReportSerializer, RoomSerializer, SendMsgSerializer, GetRoomSerializer
from user.authentication import FirebaseAuthentication

# views

@api_view(["GET"])
def userPresentOrNot(request, roomId):
    """
    Check whether chater2 is present or not
    """

    try:
        room = Room.objects.get(id=roomId)
        chater2 = room.chater2
        if chater2 == None:
         print(chater2)
         return Response({"chatter2_present": False})
        else: 
            return Response({"chatter2_present": True})
    except Users.DoesNotExist:
        return Response({"chatter2_present": False})


class GetRoomView(generics.GenericAPIView):
    serializer_class = GetRoomSerializer

    # authentication_classes = [FirebaseAuthentication]

    def post(self, request: Request, pk):
        data = request.data
        serializer = GetRoomSerializer(data = data)
        
        if serializer.is_valid():
            try:
                user = Users.objects.all().get(firebase = pk)
            except Users.DoesNotExist:
                return InvalidUserIdResponse

            if  user.ChatAllowed == False:
                return Response({"Message": "Not allowed"}, status.HTTP_403_FORBIDDEN)
  
            if Room.objects.all().exists():
                if Room.objects.filter(chater2=None).first():
                    Room1 = Room.objects.filter(chater2=None).first()

                    roomMember = Room1.chater1.firebase
                    exsistingUser = Users.objects.get(firebase = roomMember)

                    if exsistingUser.gender == user.gender:
                        new_room = Room.objects.create(chater1=user, nickname1 = data['nickname1'])
                        new_room.save()
                        respSerializer = GetRoomSerializer(new_room)
                        print("hlo2")
                        return Response(respSerializer.data, status.HTTP_201_CREATED)
                    else :
                        Room1.chater2 = user
                        Room1.nickname2 = data['nickname1']
                        Room1.save()
                        respSerializer = GetRoomSerializer(Room1)
                        print("hlo1")
                        return Response(respSerializer.data, status.HTTP_201_CREATED)

                else: 
                    new_room = Room.objects.create(chater1=user, nickname1 = data['nickname1'])
                    new_room.save()
                    respSerializer = GetRoomSerializer(new_room)
                    print("hlo3")
                    return Response(respSerializer.data, status.HTTP_201_CREATED)

            else : 
                new_room = Room.objects.create(chater1=user, nickname1 = data['nickname1'])
                new_room.save()
                respSerializer = GetRoomSerializer(new_room)
                print("hlo5")
                return Response(respSerializer.data, status.HTTP_201_CREATED)
     

class SendMsgViewSet(generics.CreateAPIView):
    serializer_class = SendMsgSerializer
    queryset =Message.objects.all()

    # authentication_classes = [FirebaseAuthentication]
    # permission_classes = (
    #     IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)


    
    def post(self,  request):
        data = request.data
        serializer = SendMsgSerializer(data=data)
        if serializer.is_valid():
            try:
                room = data['room']
                room_details = Room.objects.all().get(id=room)
            except Room.DoesNotExist:
                return Response({"Message": "Room not existed"}, status.HTTP_406_NOT_ACCEPTABLE)
            if room_details.roomBlocked == True:
                return Response({"Message": "Room Blocked"}, status.HTTP_406_NOT_ACCEPTABLE)
            else :
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class GetMessages(generics.GenericAPIView):
    serializer_class = SendMsgSerializer
    queryset =Message.objects.all()

    # authentication_classes = [FirebaseAuthentication]
    
    def get(self,request, room):
        try:
            room_details = Room.objects.get(id=room)
        except Room.DoesNotExist:
            return Response({"Message": "Room not existed"}, status.HTTP_406_NOT_ACCEPTABLE)
        messages = Message.objects.filter(room=room_details)
        return JsonResponse({"messages":list(messages.values())})



def reportView(request, firebase):
    queryset = Users.objects.filter(firebase=firebase)
    if len(queryset) > 0:
        queryset[0].ChatReports += 1
        queryset[0].save()
        if  queryset[0].ChatReports >= 3:
            queryset[0].ChatAllowed = False
            queryset[0].save()
        return HttpResponse("Reported")
    return HttpResponse("Invalid user", status.HTTP_400_BAD_REQUEST)

def blockRoom(request, room):
    try:
        room_details = Room.objects.get(id=room)
    except Room.DoesNotExist:
        return Response({"Message": "Room not existed"}, status.HTTP_406_NOT_ACCEPTABLE)

    room_details.roomBlocked = True
    return Response({"Message": "Room Blocked"}, status.HTTP_200_OK)