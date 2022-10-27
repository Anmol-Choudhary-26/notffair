from django.urls import path
from .views import GetMessages, GetRoomView, SendMsgViewSet, reportView, blockRoom, userPresentOrNot

urlpatterns = [
    path("checkchater/<str:roomId>/", userPresentOrNot),
    path('getRoom/<str:pk>/', GetRoomView.as_view(), name='getRoom'),
    path('send/<str:roomID>/<str:userID>/', SendMsgViewSet.as_view(), name='send'),
    path('getMessages/<str:room>/', GetMessages.as_view(), name='getMessages'),
    path('report/<int:firebase>/', reportView, name='reportUser'),
    path('roomBlock/<str:room>/', blockRoom, name='blockRoom'),
]