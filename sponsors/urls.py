from django.urls import path

from .views import SponsorUpdate, SponsorView

urlpatterns = [
    path('', SponsorView.as_view()),
    path('<str:pk>' , SponsorUpdate.as_view()) ,
]