from django.urls import path

from chat.views import ThreadAPIView

urlpatterns = [
    path("threads/", ThreadAPIView.as_view(), name="threads"),
    path("threads/<uuid:pk>/", ThreadAPIView.as_view(), name="thread-detail"),
]
