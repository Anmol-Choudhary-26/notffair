from django.db import models
import uuid

class Team(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    club_name = models.CharField(max_length=50,null=False,blank=False,unique=True)
    image = models.URLField('image')

    def __str__(self):
        return self.club_name

class Member(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=255, null=False)
    team_name = models.ForeignKey(Team,on_delete=models.CASCADE)
    position = models.CharField(max_length=255, null=False)
    image = models.URLField('image')

    def __str__(self):
        return self.name