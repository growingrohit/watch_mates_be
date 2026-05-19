from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import LoginAPIView, UserProfileCreateAPIView

urlpatterns = [
    path("users/", UserProfileCreateAPIView.as_view(), name="user-profile-create"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
