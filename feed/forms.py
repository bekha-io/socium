import string

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.forms import UserCreationForm, UsernameField
from captcha.fields import CaptchaField

from .models import Comment


class UserCreationWithCaptchaForm(UserCreationForm):
    captcha = CaptchaField(label="CAPTCHA")


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
