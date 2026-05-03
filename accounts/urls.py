from django.urls import path

from accounts.views import LoginAPIView, UserProfileCreateAPIView

urlpatterns = [
    path("users/", UserProfileCreateAPIView.as_view(), name="user-profile-create"),
    path("login/", LoginAPIView.as_view(), name="login"),
]
