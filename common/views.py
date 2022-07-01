from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from feed.models import Post


class SearchView(TemplateView):
    template_name = 'profile/search.html'
    http_method_names = ('get',)

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q')
        ctx = super().get_context_data(**kwargs)

        if q:
            ctx['users'] = User.objects.filter(username__icontains=q).all()
            ctx['posts'] = Post.objects.filter(text__icontains=q).order_by('-published_at')
        return ctx
