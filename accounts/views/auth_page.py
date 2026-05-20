from django.urls import reverse
from django.views.generic import TemplateView


class AuthPageView(TemplateView):
    template_name = "accounts/auth.jinja"
    default_tab = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": "Watch Mates — Sign in",
                "login_api_url": reverse("login"),
                "register_api_url": reverse("user-profile-create"),
                "default_tab": getattr(self, "default_tab", "login"),
            }
        )
        return context
