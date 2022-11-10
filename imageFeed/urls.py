from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from imageFeed.views import PostList, postView
from imageFeed import views

urlpatterns = [
      path('<str:pk>/', PostList.as_view(),name='posts'),
     path('addpost/<str:pk>/', PostList.as_view(),name='posts'),
     path('comment/<str:pk>/<str:pk1>/',
         views.AddCommentView.as_view(),
         name='add-comment'),     
     path('comment/<int:comment_id>/',
          views.ManageCommentView.as_view(),
          name='manage-comment'),
     path('like/<str:pk>/<str:pk1>',
          views.LikeView.as_view(),
          name='like'),
     path('get-likers/<uuid:post_id>/',
          views.GetLikersView.as_view(),
          name='get-likers'),
     path('getcomment/<uuid:post>/',views.getPostComments,name="get-comments"),
      path("post/<str:pk>/", postView.as_view()),
]
