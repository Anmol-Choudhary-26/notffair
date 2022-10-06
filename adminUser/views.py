from django.shortcuts import render
from django.http.response import Http404
from .models import AdminUser
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from .serializers import AdminUserSerializer

# Create your views here.

class AdminUsersView(GenericAPIView,ListModelMixin,CreateModelMixin,UpdateModelMixin):
    serializer_class = AdminUserSerializer
    queryset = AdminUser.objects.all()

    def get(self, request: Request):
        """
        Returns list of all AdminUser
        """
        return self.list(request)

    def post(self, request: Request):
        """
        Creates a AdminUser, if not exists
        """
        return self.create(request)

class AdminUserView(GenericAPIView,UpdateModelMixin, RetrieveModelMixin):
    serializer_class = AdminUserSerializer
    queryset = AdminUser.objects.all()

    def get(self, request: Request, *args, **kwargs):
        """
        Retrieve AdminUser
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        """
        Update AdminUser completely
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        """
        Update AdminUser partially
        """
        return self.partial_update(request, *args, **kwargs)