from django import http
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class LRMixin(LoginRequiredMixin):
    login_url = "/login/"

    def handle_no_permission(self) -> http.HttpResponseRedirect:
        messages.warning(
            self.request,  # type: ignore
            "you need to be logged in to gain access to this page",
        )
        return super().handle_no_permission()
