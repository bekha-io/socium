from django.urls import include, path

from .views import *

urlpatterns = [
    path('post/<int:post_id>/like', like_unlike, name='feed.like_unlike'),
    path('user/<int:following_user_id>/follow', follow_unfollow, name="profile.follow_unfollow")
]
