from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin , UpdateModelMixin , DestroyModelMixin

from .serializers import *
from .models import Sponsors


# Create your views here.

class SponsorView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = SponsorSerializer
    queryset = Sponsors.objects.all().order_by('priority')

    def get(self, request: Request):
        return self.list(request)

    
    def post(self , request , *args ,**kwargs):
        return self.create(request , *args , **kwargs)


class SponsorUpdate(GenericAPIView , RetrieveModelMixin , UpdateModelMixin , DestroyModelMixin):
    serializer_class = SponsorSerializer
    queryset = Sponsors.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)