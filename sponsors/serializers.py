from rest_framework import serializers
from .models import Sponsors

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsors
        fields = ['id', 'name', 'link', 'image', 'position', 'priority']

