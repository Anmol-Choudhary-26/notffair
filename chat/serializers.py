from rest_framework import serializers
from .models import Message, Report, Room

class GetRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['chater1', 'nickname1']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"

class SendMsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ['date']
        

