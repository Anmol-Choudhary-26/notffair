from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class AdminUser(models.Model):
    name = models.CharField("name", primary_key=True, max_length=255, unique=True, null=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='adminUser', on_delete=models.CASCADE)
    password = models.CharField('password', max_length=128, null=True, blank=True,
                         help_text='Leave empty if no change needed')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        super(AdminUser, self).save(*args, **kwargs)
        user:User = self.user
        user.password = self.password
        user.save()
        return self