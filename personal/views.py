from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, TemplateView, FormView, UpdateView, View, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest

from feed.models import Post
from .models import Profile, Following, NotificationProxy
from .forms import ProfileEditForm, UserEditForm, UserCreationWithCaptchaForm


class SignUpView(CreateView):
    form_class = UserCreationWithCaptchaForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


# Create your views here.
class ProfileUpdateView(UpdateView):
    form_class = ProfileEditForm
    context_object_name = "profile"
    template_name = 'profile/me.html'
    success_url = reverse_lazy('profile.me')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class UserUpdateView(UpdateView):
    form_class = UserEditForm
    context_object_name = "user"
    template_name = 'profile/me.html'
    success_url = reverse_lazy('profile.me')

    def get_object(self, queryset=None):
        return User.objects.get(self.request.user)


class MeUpdateView(TemplateView):
    template_name = "profile/me.html"
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        kwargs['profile'] = Profile.objects.get(user=self.request.user)
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = ProfileEditForm()
        if 'user_form' not in kwargs:
            kwargs['user_form'] = UserEditForm()
        return kwargs

    def post(self, *args, **kwargs):
        user_form, profile_form = None, None

        if 'user' in self.request.POST:
            user_form = UserEditForm(data=self.request.POST, instance=self.request.user)

        if 'profile' in self.request.POST:
            profile_form = ProfileEditForm(data=self.request.POST,
                                           instance=self.request.user.profile)

        if user_form and user_form.is_valid():
            username, password = user_form.cleaned_data['username'], user_form.cleaned_data['password']
            self.request.user.username = username
            self.request.user.set_password(password)
            self.request.user.save()

            user = authenticate(username=username, password=password)
            login(self.request, user)

        if profile_form and profile_form.is_valid():
            profile_form.save()

        return redirect('profile.me')


class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = "profile"
    template_name = "profile/guest.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            return redirect(reverse('profile.me'))
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["posts"] = self.object.user.posts.all()
        is_following = True if self.request.user.following.filter(following_user=self.object.user) else False
        ctx["is_following"] = is_following
        return ctx

    def get_object(self, queryset=None):
        profile = super().get_object(queryset)
        return profile


class SearchView(TemplateView):
    template_name = 'profile/search.html'
    http_method_names = ('get')

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q')
        print(q)
        ctx = super().get_context_data(**kwargs)

        if q:
            ctx['users'] = User.objects.filter(username__contains=q).all()
            ctx['posts'] = Post.objects.filter(text__contains=q).order_by('-published_at')[:20]

        return ctx


class MyNotificationsView(TemplateView):
    template_name = 'profile/notifications.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['notifications'] = NotificationProxy.objects.filter(recipient=self.request.user)
        return ctx
