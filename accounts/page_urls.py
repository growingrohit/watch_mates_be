from django.urls import path

from accounts.views import AuthPageView

urlpatterns = [
    path("login/", AuthPageView.as_view(), name="auth-login-page"),
    path(
        "register/",
        AuthPageView.as_view(default_tab="register"),
        name="auth-register-page",
    ),
]
