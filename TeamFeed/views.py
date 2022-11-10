from rest_framework import permissions, viewsets, generics, status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import TeamPostSerializer, TeamCommentSerializer, UserSerializerforImagefeed, TeamLikeSerializer
from .models import TeamPost, TeamComment
from user.models import Users
from rest_framework.request import Request
from rest_framework.authentication import SessionAuthentication
from .permissions import IsOwnerOrReadOnly, IsOwnerOrPostOwnerOrReadOnly
from .pagination import FollowersLikersPagination
from Utils.helper_response import InvalidUserIdResponse
from rest_framework.generics import GenericAPIView
from django.http.response import Http404
from rest_framework.mixins import ListModelMixin , CreateModelMixin , UpdateModelMixin , RetrieveModelMixin , DestroyModelMixin
from django.http import JsonResponse
from user.authentication import FirebaseAuthentication
from .pagination import PageNumberPagination, PostsPagination

class PostList(GenericAPIView , ListModelMixin , CreateModelMixin):
    serializer_class = TeamPostSerializer
    # pagination_class = PostsPagination

    # authentication_classes = [FirebaseAuthentication]
    # permission_classes = (
    #     IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)

    def get_queryset(self):

        id = self.kwargs['pk']
        user = Users.objects.get(firebase=id)
        posts = TeamPost.objects.all()
        for post in posts:
            a = True
            for u in post.likes.all():
                if u == user:
                    a = False
                    post.islikedbycurrentuser = True
                    post.save()
                    break
            if a == True:
                post.islikedbycurrentuser = False
                post.save()

        queryset = TeamPost.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, pk):
        data = request.data
        serializer = TeamPostSerializer(data=data)
        if serializer.is_valid():
            try:
                user = Users.objects.all().get(firebase = pk)
            except Users.DoesNotExist:
                return InvalidUserIdResponse

            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentView(generics.CreateAPIView):
    serializer_class = TeamCommentSerializer

    # authentication_classes = [FirebaseAuthentication]
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def post(self, request: Request, pk, pk1):
        data = request.data
        serializer = TeamCommentSerializer(data=data)
        if serializer.is_valid():
            try:
                post = TeamPost.objects.get(id = pk)
            except TeamPost.DoesNotExist:
                return Response({"Message": "Invalid Post"}, status.HTTP_404_NOT_FOUND)
            
            try:
                user = Users.objects.all().get(firebase = pk1)
            except Users.DoesNotExist:
                return InvalidUserIdResponse

            serializer.save(post=post, author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ManageCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamCommentSerializer
    lookup_url_kwarg = 'comment_id'

    # authentication_classes = [FirebaseAuthentication]
    # permission_classes = (IsOwnerOrPostOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = TeamComment.objects.all()
        return queryset


class LikeView(GenericAPIView):
    serializer_class = TeamLikeSerializer
    """Toggle like"""

    # authentication_classes = [FirebaseAuthentication]
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request,pk, pk1):
        data = request.data
        serializer = TeamLikeSerializer(data=data)
        if serializer.is_valid():
            try:
                post = TeamPost.objects.all().get(id = pk)
            except TeamPost.DoesNotExist:
                return Response({"Message": "Invalid Post"}, status.HTTP_404_NOT_FOUND)
            
            try:
                user = Users.objects.all().get(firebase = pk1)
            except Users.DoesNotExist:
                return InvalidUserIdResponse

        like = False
        updated = False
    
        profile =user
        if profile in post.likes.all():
            like = False
            user.score =user.score - 1
            user.save()
            
            post.likes.remove(profile)
        else:
            like = True
            user.score =user.score + 1
            user.save()
            post.likes.add(profile)

            updated = True
        data = {
            'like': like,
            'updated' : updated
        }
        return Response(data)


class GetLikersView(generics.ListAPIView):
    serializer_class = UserSerializerforImagefeed
    pagination_class = FollowersLikersPagination

    # authentication_classes = [FirebaseAuthentication]
    # permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = TeamPost.objects.get(
            pk=post_id).likes.all()
        return queryset


def getPostComments(request, post):
    getpost = TeamPost.objects.get(id=post)
    commenters = TeamComment.objects.filter(post = getpost)
    fmembers = []
    for member in commenters:
        m = {

            "id" : member.id,
            "author" : str(member.author),
            "author_firebaseID": member.author.firebase,
            "text" : member.text,
            "posted_on" : member.posted_on

        }
        fmembers.append(m)
        
    map1 = {
        f"{post}'scommenters":fmembers
    }
    return JsonResponse(map1,safe=False)


class TeampostView(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    serializer_class =  TeamPostSerializer

    def get_queryset(self, pk=None):
        try:
            if pk == None:
                return TeamPost.objects.all()
            return TeamPost.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk):
        """
        Returns user with given firebase id
        """
        post = TeamPostSerializer(self.get_queryset(pk))
        return Response(post.data)

    def put(self, request: Request, *args, **kwargs):
        """
        Updates user with given firebase id
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)