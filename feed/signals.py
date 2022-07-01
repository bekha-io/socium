import typing

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from notifications.signals import notify
from notifications.models import Notification

from .models import PostLike, Post, Comment
from personal.models import User


class NotificationVerbs:
    HAS_LIKED_YOUR_POST = "нравится ваша публикация"
    HAS_MENTIONED_YOU = "отметил вас в публикации"
    HAS_COMMENTED_YOUR_POST = "прокомментировал вашу публикацию"
    HAS_MENTIONED_YOU_IN_COMMENTS = "отметил вас в комментариях к публикации"


def extract_mention(text: str) -> typing.List['User']:
    mentioned = []
    for word in text.split():
        if word[0] == '@':
            try:
                username = word[1:]
                user = User.objects.get(username=username)
                if user:
                    mentioned.append(user)
            except User.DoesNotExist:
                continue
    return mentioned


@receiver(post_save, sender=Post)
def post_created_handler(sender: Post, instance: Post, created: bool, **kwargs):
    if created:
        mentioned_users = extract_mention(instance.text)
        for mentioned in mentioned_users:
            notify.send(instance.author, recipient=mentioned, verb=NotificationVerbs.HAS_MENTIONED_YOU,
                        action_object=instance)


@receiver(post_save, sender=PostLike)
def like_post_handler(sender: PostLike, instance: PostLike, created: bool, **kwargs):
    if created and instance.user != instance.post.author:
        notify.send(instance.user, recipient=instance.post.author,
                    verb=NotificationVerbs.HAS_LIKED_YOUR_POST, action_object=instance.post)


@receiver(post_delete, sender=PostLike)
def unlike_post_handler(sender: PostLike, instance: PostLike, **kwargs):
    Notification.objects.filter(recipient=instance.post.author,
                                actor_object_id=instance.user.id,
                                verb=NotificationVerbs.HAS_LIKED_YOUR_POST,
                                action_object_object_id=instance.post.id).delete()


@receiver(post_save, sender=Comment)
def new_comment_handler(sender: Comment, instance: Comment, created: bool, **kwargs):
    if created:
        if instance.author != instance.post.author:
            notify.send(instance.author, recipient=instance.post.author,
                        verb=NotificationVerbs.HAS_COMMENTED_YOUR_POST,
                        target=instance.post)

        # Checking is any user mentioned, then sending notification if any
        mentioned = extract_mention(instance.text)
        for mentioned_id in mentioned:
            notify.send(instance.author, recipient=mentioned_id,
                        verb=NotificationVerbs.HAS_MENTIONED_YOU_IN_COMMENTS,
                        target=instance.post)


# @receiver(post_delete, sender=Comment)
# def comment_deleted_handler(sender: Comment, instance: Comment, **kwargs):
#     Notification.objects.filter(recipient=instance.post.author,
#                                 verb=NotificationVerbs.HAS_COMMENTED_YOUR_POST,
#                                 target=instance.post,
#                                 actor_object_id=instance.author.id).delete()
