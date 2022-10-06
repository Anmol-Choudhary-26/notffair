from dataclasses import field, fields
from pyexpat import model
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from .models import AdminUser
from django.contrib.auth.models import User


class AdminUserSerializer(ModelSerializer):
    class Meta:
        model = AdminUser

        fields = ['name', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4,
                                     'style': {'input_type': 'password', 'placeholder': 'Password', 'required': False}}}

    def save(self, **kwargs):
        password = self.validated_data.get("password", '')
        if password == '' and self.instance is not None:
            password = self.instance.password
        else:
            password = make_password(password)
        self.validated_data.update({'password': password})
        return super().save(**kwargs)

    def create(self,validated_data):
        adminUser = AdminUser(
            name = validated_data['name'],
            password = validated_data['password']
        )
        adminUser.user = User(username=validated_data["name"], password=validated_data["password"])
        adminUser.user.save()
        adminUser.save()
        return adminUser
