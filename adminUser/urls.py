from django.urls import path

from .views import AdminUserView, AdminUsersView

urlpatterns = [
    path("", AdminUsersView.as_view()),
    path("<str:pk>", AdminUserView.as_view()),
]