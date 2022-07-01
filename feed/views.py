from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView, CreateView, DeleteView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .forms import CommentCreateForm
from .models import Post, PostLike, Comment

from .services import *


class MyFeedView(CreateView):
    model = Post
    fields = ['text']
    template_name = "feed/my_feed.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        feed_type = self.request.GET.get('feed')
        ctx = super().get_context_data(**kwargs)

        if not feed_type:
            feed_type = 'new' if not self.request.user.is_authenticated else 'following'

        if feed_type == 'following':
            try:
                ctx['following_posts'] = get_my_and_following_posts(self.request.user)
            except Post.DoesNotExist:
                pass

        elif feed_type == 'new':
            ctx['latest_posts'] = get_latest_posts()

        return ctx

    def post(self, request, *args, **kwargs):
        post = Post(text=self.request.POST['text'], author=self.request.user)
        post.save()
        return redirect('home')


class MyPostsList(CreateView):
    model = Post
    fields = ['text']
    template_name = 'feed/my_posts.html'
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['my_posts'] = get_my_posts(self.request.user)
        return ctx

    def post(self, request, *args, **kwargs):
        post = Post(text=self.request.POST['text'], author=self.request.user)
        post.save()
        return redirect('feed.my_posts')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = self.object.comments.all()
        ctx['comment_form'] = CommentCreateForm()
        return ctx

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        return post

    def post(self, request, *args, **kwargs):
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid() and self.request.user.is_authenticated:
            comment_text = comment_form.cleaned_data['text']
            Comment(author=self.request.user,
                    post=self.get_object(), text=comment_text).save()
        return redirect('feed.post_detail', pk=self.get_object().pk)


class DeletePost(DeleteView):
    success_url = reverse_lazy('home')
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author == self.request.user or self.request.user.is_superuser:
            return post
