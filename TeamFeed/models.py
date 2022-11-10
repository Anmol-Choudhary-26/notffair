from email.policy import default
from django.db import models
from user.models import Users
import uuid
# Create your models here.


class TeamPost(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='Team_posts'
    )
    islikedbycurrentuser = models.BooleanField(default=False)
    isVid = models.BooleanField(default=False)
    photo = models.URLField(max_length=255,null=True, blank=False)
    text = models.TextField(max_length=500, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Users,
                                   related_name="TeamPost_likers",
                                   blank=True,
                                   symmetrical=False)

    class Meta:
        ordering = ['-posted_on']

    def number_of_likes(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0

    def __str__(self):
        return f'{self.author}\'s post'


class TeamComment(models.Model):
    post = models.ForeignKey('TeamPost',
                             on_delete=models.CASCADE,
                             related_name='Teampost_comments')
    author = models.ForeignKey(Users,
                               on_delete=models.CASCADE,
                               related_name='Teampost_comments')
    text = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f'{self.author}\'s comment'