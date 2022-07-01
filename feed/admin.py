from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'text', 'published_at', 'edited_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
