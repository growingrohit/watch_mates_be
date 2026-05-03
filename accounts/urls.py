from django.urls import path

from accounts.views import UserProfileCreateAPIView

urlpatterns = [
    path("users/", UserProfileCreateAPIView.as_view(), name="user-profile-create"),
]
