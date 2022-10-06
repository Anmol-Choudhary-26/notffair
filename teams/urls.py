from . import views
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('team',TeamViewset,basename="teams")
router.register('member',MemberViewset,basename="members")

urlpatterns = [
    path('',include(router.urls)),
    path('<str:team>',views.getteammembers,name="helo")
]