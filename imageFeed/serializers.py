from .models import Post, Comment
from rest_framework import serializers
from user.models import Users
from django.core.paginator import Paginator
from user.serializers import UserSerializerforImagefeed


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the comment objects
    """
    class Meta:
        model = Comment
        fields = [ 'text']
       
    # def create(self,validated_data):
    #     author = Users(
    #         name = validated_data['name'],
           
    #     )
    #     author.user = Users(username=validated_data["name"])
    #     author.user.save()
    #     author.save()
    #     return author


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the post objects
    """

    author = UserSerializerforImagefeed(read_only=True)
    # photo = serializers.URLField(max_length=None, allow_empty_file=False)
    number_of_comments = serializers.SerializerMethodField()
    # post_comments = serializers.SerializerMethodField(
    #     'paginated_post_comments')
    # liked_by_req_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author',  'photo',
                  'text', 'posted_on', 'islikedbycurrentuser',
                  'number_of_likes', 'number_of_comments'
                  ]

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()

    # def paginated_post_comments(self, obj):
    #     page_size = 2
    #     paginator = Paginator(obj.post_comments.all(), page_size)
    #     page = self.context['request'].query_params.get('page') or 1

    #     post_comments = paginator.page(page)
    #     serializer = CommentSerializer(post_comments, many=True)

    #     return serializer.data

    def get_liked_by_req_user(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()
    
    # def create(self,validated_data):
    #     author = User(
    #         name = validated_data['username'],
           
    #     )
    #     author.user = User(username=validated_data["username"])
    #     author.user.save()
    #     author.save()
    #     return author

class LikeSerializer(serializers.Serializer):
    class Meta:
        model : Post
        