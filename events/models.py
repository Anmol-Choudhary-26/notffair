from django.db import models
from uuid import uuid4

class Events(models.Model):
    title = models.CharField(primary_key=True , max_length=100 , null=False)
    description = models.CharField(max_length=300 , null=True)
    startTime = models.DateTimeField("start",null = True)
    endTime = models.DateTimeField("end",null = True)
    clubName = models.CharField(max_length=50 , null = False)
    platform = models.URLField(null=True)
    image = models.URLField("Image Url", null=True,blank=True)
    regURL = models.URLField("regURL", blank=True, null=True)

    EVENTS = 0
    WORKSHOP = 1

    choices = (
        (0, EVENTS),
        (1, WORKSHOP)
    )
    type = models.IntegerField("type", choices = choices)

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        if self.type == 0:
            return f"<Events: {self.__str__()}>"
        if self.type == 1:
            return f"<Workshop: {self.__str__()}>"