from django.contrib import admin
from .models import Room, Message, Report

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Report)