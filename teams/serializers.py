from rest_framework import serializers
from .models import Member, Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','club_name','image']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id','name','team_name','position', 'image']
