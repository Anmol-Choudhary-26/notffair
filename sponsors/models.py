from django.db import models

# Create your models here.

class Sponsors(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField('image', null=True, blank=True)
    link = models.URLField('link', null=True, blank=True)
    position = models.CharField("position", max_length= 255, null=True, blank=True)
    priority = models.IntegerField("priority", default=1)

    def __str__(self):
        print(self.name)
        if self.name is None:
            return f"sponsor: NoName"
        return f"sponsor: {self.name}"