from django.urls import include, path

from .views import *


urlpatterns = [
    path('', MeUpdateView.as_view(), name="profile.me"),
    path('signup/', SignUpView.as_view(), name="profile.signup"),
    path('<int:pk>', login_required(ProfileDetailView.as_view()), name="profile.guest"),

    path('notifications/', MyNotificationsView.as_view(), name='profile.notifications'),

    path('following', login_required(MyFollowingView.as_view()), name="profile.following"),
]
