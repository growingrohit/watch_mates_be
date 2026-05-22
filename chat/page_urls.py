from django.urls import path

from chat.views.pages import ThreadDetailPageView, ThreadsListPageView

urlpatterns = [
    path("threads/", ThreadsListPageView.as_view(), name="chat-threads-page"),
    path(
        "threads/<uuid:thread_id>/",
        ThreadDetailPageView.as_view(),
        name="chat-thread-detail-page",
    ),
]
