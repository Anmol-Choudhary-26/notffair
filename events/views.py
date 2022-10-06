from django.shortcuts import render
from .models import Events
from .serializers import EventSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin , CreateModelMixin , UpdateModelMixin , RetrieveModelMixin , DestroyModelMixin
from datetime import datetime
# Create your views here.

class EventList(GenericAPIView , ListModelMixin , CreateModelMixin):
    serializer_class = EventSerializer
    
    def get_queryset(self):
        queryset = Events.objects.all().order_by('startTime')
        
        if self.request.query_params.get('type') == 'events':
            queryset = queryset.filter(Type=0)
        elif self.request.query_params.get('type') == 'workshop':
            queryset = queryset.filter(Type=1)

        if self.request.query_params.get('date', None) != None:
            datestr = self.request.query_params.get('date', None)
            format = "%Y-%m-%dT%H:%M:%S%z"
            datestr = ''.join(datestr.rsplit(":",1))
            try:
                date = datetime.strptime(datestr, format)
                queryset = queryset.filter(start__gte=date)
            except:
                pass
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self , request , *args ,**kwargs):
        return self.create(request , *args , **kwargs)

class EventAccess(GenericAPIView , RetrieveModelMixin , UpdateModelMixin , DestroyModelMixin):
    serializer_class = EventSerializer
    queryset = Events.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
