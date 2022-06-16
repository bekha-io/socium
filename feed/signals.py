from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from notifications.signals import notify
from notifications.models import Notification

from .models import PostLike


class NotificationVerbs:
    HAS_LIKED_YOUR_POST = "нравится ваша публикация"


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
