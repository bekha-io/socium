from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from feed.models import Post, PostLike, Comment


@login_required
@csrf_exempt
def like_unlike(request: HttpRequest, post_id: int):
    if request.user.is_anonymous:
        return redirect(reverse('login'))

    post = Post.objects.get(id=post_id)

    if post.likes.filter(user=request.user):
        post.likes.filter(user=request.user).delete()
        return JsonResponse(
            data={
                "status": "fail",
                "data": {"post":
                    {
                        "likes": post.likes_count
                    }
                }
            }
        )

    else:
        PostLike.objects.create(user=request.user, post=post)
        return JsonResponse(
            data={
                "status": "success",
                "data": {"post":
                    {
                        "likes": post.likes_count}
                }
            }
        )


@login_required
@csrf_exempt
def follow_unfollow(request, following_user_id: int):
    following_user = User.objects.get(id=following_user_id)

    if following_user == request.user:
        return redirect('profile.guest', pk=following_user_id)

    if request.user.following.filter(following_user=following_user):
        request.user.following.filter(following_user=following_user).delete()

    else:
        request.user.following.create(user=request.user,
                                      following_user=following_user)

    return redirect('profile.guest', pk=following_user_id)


@login_required
@csrf_exempt
def comment_delete(request, comment_id: int):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponse(status=404)

    if request.user == comment.author or request.user == comment.post.author \
            or request.user.is_superuser:
        comment.soft_delete()
        return JsonResponse(
            data={
                "status": "success",
            })
    else:
        return HttpResponse(status=403)
