from django import template
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='mention')
@stringfilter
def mention(value, template_name='user_mention_inline'):
    """Searches for any @ user mention in the given text and renders a userMention snippet"""
    words = value.split()
    for word in words:
        if word[0] == '@':
            try:
                username = word[1:]
                user = User.objects.get(username=username)
                if user:
                    user_mention = render_to_string(f'./snippets/{template_name}.html',
                                                    context={'profile': user.profile})
                    value = value.replace(word, user_mention)
            except User.DoesNotExist:
                continue
    return mark_safe(value)


@register.filter(name='mention_raw')
@stringfilter
def mention_raw(value: str):
    """Searches for any raw users mention in the given text and compares each word with list of existing users"""
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
