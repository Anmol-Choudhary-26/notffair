from django.db import models
from datetime import datetime
from user.models import Users
import uuid

# Create your models here.
class Room(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    chater1 = models.ForeignKey(Users, on_delete=models.CASCADE,related_name="chater1")
    nickname1 = models.CharField(max_length= 100,  default="NoName1")
    chater2 = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name="chater2")
    nickname2 = models.CharField(max_length= 100, default="Noname2")
    roomBlocked = models.BooleanField('RoomBlocked', default=False)

    

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE,)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

class Report(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reporter = models.ForeignKey(Users, related_name='reporter_user', on_delete=models.CASCADE)
    reported = models.ForeignKey(Users, related_name='reported_user', on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return (
            self.room + ' - '
            + self.reporter.username + ' - '
            + 'reported - '
            + self.reported.username + ' - '
            + self.reason
        )