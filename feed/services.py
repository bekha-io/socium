import typing
from itertools import chain

from .models import Post
from django.contrib.auth.models import User


def get_latest_posts() -> typing.List[Post]:
    return Post.objects.all().order_by('-published_at')[:20]


def get_following_posts(user: User) -> typing.List[Post]:
    return Post.objects.filter(author__followers__user=user).order_by('-published_at')[:20]


def get_my_posts(user: User):
    return Post.objects.filter(author=user).order_by('-published_at')


def get_my_and_following_posts(user: User):
    return reversed(sorted(chain(get_my_posts(user), get_following_posts(user)), key=lambda i: i.published_at))