from django import template
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='mention', is_safe=True)
@stringfilter
def mention(value):
    words = value.split()
    for word in words:
        if word[0] == '@':
            try:
                username = word[1:]
                user = User.objects.get(username=username)
                if user:
                    user_mention = render_to_string("./snippets/user_mention_inline.html",
                                                    context={'profile': user.profile})
                    value = value.replace(word, user_mention)
            except User.DoesNotExist:
                continue
    return mark_safe(value)


@register.filter(name='mention_raw', is_safe=True)
@stringfilter
def mention_raw(value: str):
    counter = 0
    words: list[str] = value.split()
    for i in range(0, len(words)):
        try:
            user = User.objects.get(username=words[i])
            if user:
                user_mention = render_to_string("./snippets/user_mention_inline.html",
                                                context={'profile': user.profile})
                words[i] = user_mention
        except User.DoesNotExist:
            continue
    return mark_safe(" ".join(words))
