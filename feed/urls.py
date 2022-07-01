from django.urls import include, path

from .views import *

urlpatterns = [
    path('', MyFeedView.as_view(), name='home'),
    path('user/posts', login_required(MyPostsList.as_view()), name="feed.my_posts"),

    path('post/<int:pk>', PostDetailView.as_view(), name="feed.post_detail"),
    path('post/<int:pk>/delete', login_required(DeletePost.as_view()), name="feed.delete_post"),
]
