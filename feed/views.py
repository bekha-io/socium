from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView, CreateView, DeleteView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Post, PostLike

from .services import *


class MyFeedView(CreateView):
    model = Post
    fields = ['text']
    template_name = "feed/my_feed.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            if self.request.user.is_authenticated:
                ctx['following_posts'] = get_my_and_following_posts(self.request.user)
            ctx['latest_posts'] = get_latest_posts()
        except Post.DoesNotExist:
            pass
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

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        return post


class DeletePost(DeleteView):
    success_url = reverse_lazy('home')
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author == self.request.user or self.request.user.is_superuser:
            return post
