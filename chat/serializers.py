from rest_framework import serializers
from .models import Message, Report, Room

class GetRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = ['chater1','chater2','roomBlocked', 'nickname2']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"

class SendMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['value']
        read_only_fields = ['date']
        

