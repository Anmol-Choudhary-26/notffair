from http.client import HTTPResponse
import logging
from django.http.response import Http404
from rest_framework.decorators import api_view
from .models import Users
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_404_NOT_FOUND

from user.serializers import UserSerializer

# Logger
logger = logging.getLogger(__name__)



@api_view(["GET"])
def userPresentOrNot(request, email):
    """
    Check whether a user is present or not
    Based on User Email Id
    """
    print(email)
    try:
        user = Users.objects.get(email=email)
        print(user)
        m = {

             "first_name": user.first_name,
    "last_name": user.last_name,
    "firebase": user.firebase,
    "name": user.name,
    "gender": user.gender,
    "phone": user.phone,
    "ChatAllowed": user.ChatAllowed,
    "ChatReports": user.ChatReports,
    "email": user.email,
    "score": user.score,
    "instagramId": user.instagramId,
    "profileImage": user.profileImage
        }
        print("kd")
        # return HTTPResponse("<h1>la</h1>")
        # return JsResponse({"firebaseid":})
        return JsonResponse(m)
    except Users.DoesNotExist:
        return Response({"user_present": False})


class UsersView(GenericAPIView):
    serializer_class = UserSerializer

    queryset = Users.objects.all()

    def get(self, request):
        """
        Returns list of all users
        """
        users = UserSerializer(self.get_queryset(), many=True)
        return Response(users.data)

    def post(self, request: Request):
        """
        Creates a user, if not already exists
        """
        try:
            user = UserSerializer(data=request.data)
            if user.is_valid():
                user.save()
                return Response(data=user.data, status=HTTP_201_CREATED)
            else:
                data = {"Message": "Invalid user data", "Errors:": user.errors}
                return Response(data=data, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(e)
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserView(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    serializer_class = UserSerializer

    def get_queryset(self, pk=None):
        try:
            if pk == None:
                return Users.objects.all()
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk):
        """
        Returns user with given firebase id
        """
        user = UserSerializer(self.get_queryset(pk))
        return Response(user.data)

    def put(self, request: Request, *args, **kwargs):
        """
        Updates user with given firebase id
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)