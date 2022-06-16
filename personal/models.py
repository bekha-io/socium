import random
import string

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import get_language, to_locale
from django.contrib.humanize.templatetags.humanize import naturaltime
from notifications.models import Notification


def generate_default_username():
    s = ""
    for i in range(0, 12):
        s += random.choice(string.ascii_lowercase)
    return s


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True)

    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)

    avatar_url = models.URLField()

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def mention(self):
        return f"@{self.user.username}"

    @property
    def followers_count(self):
        return self.user.following.count()

    @property
    def following_count(self):
        return self.user.followers.count()

    @property
    def total_likes_count(self):
        return sum(i.likes_count for i in self.user.posts.all())


@receiver(post_save, sender=User)
def create_models_after_register(sender: User, instance: User, created: bool, *args, **kwargs):
    if created:
        p = Profile.objects.create(user=instance)
        p.save()


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'following_user')


class NotificationProxy(Notification):
    class Meta:
        proxy = True

    def __str__(self):

        # lang = get_language()
        # if lang:
        #     _ = i18n.activate(to_locale(lang))

        # For more correct output of notification in templates (timesince has been changed to humanize)
        ctx = {
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object,
            'target': self.target,
            'timesince': naturaltime(self.timestamp)
        }
        if self.target:
            if self.action_object:
                return u'%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s' % ctx
            return u'%(actor)s %(verb)s %(target)s %(timesince)s' % ctx
        if self.action_object:
            return u'%(actor)s %(verb)s %(action_object)s %(timesince)s' % ctx
        return u'%(actor)s %(verb)s %(timesince)s' % ctx
