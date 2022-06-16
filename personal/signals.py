from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from notifications.signals import notify
from .models import Following, Notification


class NotificationVerbs:
    HAS_FOLLOWED_YOU = "подписался на вас"


@receiver(post_save, sender=Following)
def follow_user_handler(sender: Following, instance: Following, created, **kwargs):
    if created and instance.user != instance.following_user:
        notify.send(instance.user, recipient=instance.following_user,
                    verb=NotificationVerbs.HAS_FOLLOWED_YOU)


@receiver(post_delete, sender=Following)
def unfollow_user_handler(sender: Following, instance: Following, **kwargs):
    Notification.objects.filter(recipient=instance.following_user,
                                actor_object_id=instance.user.id,
                                verb=NotificationVerbs.HAS_FOLLOWED_YOU).delete()