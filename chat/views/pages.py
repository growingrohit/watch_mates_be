from django.urls import reverse
from django.views.generic import TemplateView


class ChatPageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "threads_api_url": reverse("threads"),
                "login_page_url": reverse("auth-login-page"),
            }
        )
        return context


class ThreadsListPageView(ChatPageView):
    template_name = "chat/threads.jinja"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Watch Mates — Chats"
        return context


class ThreadDetailPageView(ChatPageView):
    template_name = "chat/thread_detail.jinja"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread_id = kwargs.get("thread_id")
        context.update(
            {
                "page_title": "Watch Mates — Chat",
                "thread_id": thread_id,
                "thread_detail_api_url": reverse("thread-detail", kwargs={"pk": thread_id}),
                "thread_messages_api_url": reverse(
                    "thread-messages",
                    kwargs={"thread_id": thread_id},
                ),
            }
        )
        return context
