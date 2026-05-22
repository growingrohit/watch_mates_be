from django.urls import path

from chat.views import ThreadAPIView, ThreadMessageAPIView

urlpatterns = [
    path("threads/", ThreadAPIView.as_view(), name="threads"),
    path("threads/<uuid:pk>/", ThreadAPIView.as_view(), name="thread-detail"),
    path(
        "threads/<uuid:thread_id>/messages/",
        ThreadMessageAPIView.as_view(),
        name="thread-messages",
    ),
    path(
        "threads/<uuid:thread_id>/messages/<uuid:pk>/",
        ThreadMessageAPIView.as_view(),
        name="thread-message-detail",
    ),
]
