from django.urls import path
from .views import EventList, EventAccess

urlpatterns = [
    path('' , EventList.as_view()) ,
    path('<str:pk>' , EventAccess.as_view()) ,
]
