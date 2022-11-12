from django.urls import path

from .views import UserView, UsersView, userPresentOrNot
from .authentication import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", UsersView.as_view()),
    path("<str:pk>/", UserView.as_view()),
    path("checkUser/<str:email>", userPresentOrNot)
]