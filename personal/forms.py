import string

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.forms import UserCreationForm, UsernameField
from captcha.fields import CaptchaField

from .models import Profile


class UserCreationWithCaptchaForm(UserCreationForm):
    captcha = CaptchaField(label="CAPTCHA")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar_url']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    password_confirm = forms.CharField(label="Подтверждение пароля")

    def clean(self):
        data = super().clean()
        username: str = data.get("username")
        password = data.get("password")
        password_c = data.get("password_confirm")

        for s in username:
            if s not in string.ascii_letters + string.digits:
                raise forms.ValidationError("Non alphabet or numeric symbols are not allowed to use in username")

        if password != password_c:
            raise forms.ValidationError("Password and password confirmation do not match!")