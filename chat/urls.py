from django.urls import path
from .views import GetMessages, GetRoomView, SendMsgViewSet, reportView, blockRoom

urlpatterns = [
  
    path('getRoom/', GetRoomView.as_view(), name='getRoom'),
    path('send/', SendMsgViewSet.as_view(), name='send'),
    path('getMessages/<str:room>/', GetMessages.as_view(), name='getMessages'),
    path("report/<int:firebase>/", reportView, name='reportUser'),
    path("roomBlock/<str:room>/", blockRoom, name='blockRoom'),
]