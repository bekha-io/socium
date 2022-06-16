from django.contrib import admin
from .models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'avatar_url', 'created_at', 'updated_at')
