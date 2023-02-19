from typing import Any

from django import http
from django import shortcuts
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from app_main.models import Profile

User = get_user_model()


class AuthHelperMixin(AccessMixin):
    def handle_no_permission(self, *args: Any) -> http.HttpResponseRedirect:
        if (
            self.request.user.is_authenticated  # type: ignore
            or "permission" in args
        ):
            messages.warning(
                self.request,  # type: ignore
                "you don't have enough permissions to access this page",
            )
            return shortcuts.redirect("/")
        elif (
            not self.request.user.is_authenticated  # type: ignore
            or "login" in args
        ):
            messages.warning(
                self.request,  # type: ignore
                "you need to be logged in to gain access to this page",
            )
        return super().handle_no_permission()


class LRMixin(LoginRequiredMixin, AuthHelperMixin):
    login_url = "/login/"


class RoleUPTMixin(UserPassesTestMixin, AuthHelperMixin):
    role_required: str

    def test_func(self) -> Any:
        usr_rq = self.request.user  # type: ignore
        usr = User.objects.get(id=usr_rq.pk)
        if usr.is_superuser:
            return 1
        prf = Profile.objects.get(user_id=usr.pk)
        prf_rl = prf.role
        return prf_rl == self.role_required
