from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.html import strip_tags


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(max_length=256)

    published_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def get_url(self):
        return f'/post/{self.pk}'

    def __str__(self):
        return f"<a href='{self.get_url()}'>{strip_tags(self.text[:20])}...</a>"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def liked_by_users(self):
        return [i.user for i in self.likes.filter()]


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts_liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
