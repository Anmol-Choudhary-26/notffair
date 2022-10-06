
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import *
from .models import Member,Team


class TeamViewset(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class MemberViewset(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

def getteammembers(request,team):
    getteam = Team.objects.get(club_name=team)
    members = Member.objects.filter(team_name=getteam.id)
    fmembers = []
    for member in members:
        m = {
            "id" : member.id,
            "name" : member.name,
            "team_name" : str(member.team_name),
            "position" : member.position,
            "image" : member.image
        }
        fmembers.append(m)
        
    map1 = {
        f'{team}Members':fmembers
    }
    return JsonResponse(map1,safe=False)