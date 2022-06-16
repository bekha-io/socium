from django.urls import include, path

from .views import *


urlpatterns = [
    path('', MeUpdateView.as_view(), name="profile.me"),
    path('signup/', SignUpView.as_view(), name="profile.signup"),
    path('<int:pk>', ProfileDetailView.as_view(), name="profile.guest"),

    path('search/', SearchView.as_view(), name="search"),
    path('notifications/', MyNotificationsView.as_view(), name='profile.notifications')
]
