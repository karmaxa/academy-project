from typing import Any

from django import http
from django import shortcuts
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin

from app_main.helpers import roles_priorities
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
        prf_rl_prior = roles_priorities[prf_rl]
        return prf_rl_prior >= roles_priorities[self.role_required]


class ProfileSingleObjectMixin(LRMixin, SingleObjectMixin):
    def handle_no_permission(  # type: ignore
        self, *args: Any
    ) -> http.HttpResponseRedirect:
        from app_main.views.logic.helpers import get_user_role

        u_role = get_user_role(self.request)  # type: ignore
        if u_role != "director":
            from app_main.views.logic.helpers import get_user_profile

            u_profile = get_user_profile(self.request, "self")  # type: ignore
            if u_profile.user != self.request.user:  # type: ignore
                return super().handle_no_permission(self, "permission")

    def get_object(self, queryset=None) -> Any:  # type: ignore
        if not self.request.resolver_match.kwargs.get("pk"):  # type: ignore
            from app_main.views.logic.helpers import get_user_profile

            return get_user_profile(self.request, "self")  # type: ignore
        else:
            return super().get_object()

    def get_context_data(self, **kwargs: dict) -> Any:
        ctx = super().get_context_data()
        from app_main.views.logic.helpers import get_current_student
        from app_main.views.logic.helpers import get_user_classrooms

        if self.request.resolver_match.kwargs.get("pk"):  # type: ignore
            classrooms = get_user_classrooms(
                self.request, "path"  # type: ignore
            )
            ctx["classrooms"] = classrooms
            current_student = get_current_student(
                self.request, None, "path"  # type: ignore
            )
            ctx["current_student"] = current_student
        else:
            classrooms = get_user_classrooms(
                self.request, "self"  # type: ignore
            )
            ctx["classrooms"] = classrooms
            current_student = get_current_student(
                self.request, None, "self"  # type: ignore
            )
            ctx["current_student"] = current_student
            ctx["email"] = (
                self.object.email if self.object.email else ""  # type: ignore
            )
        return ctx
