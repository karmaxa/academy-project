from typing import Any

from django import forms
from django import http
from django.contrib.auth import get_user_model
from django.views import generic

from app_main.helpers import roles
from app_main.mixins import LRMixin
from app_main.mixins import ProfileSingleObjectMixin
from app_main.mixins import RoleUPTMixin
from app_main.models import Profile

User = get_user_model()


class AllUsersView(LRMixin, RoleUPTMixin, generic.ListView):
    role_required: str = "director"
    template_name = "app_main/allusers.html"
    model = Profile
    extra_context = {"roles": [role[0] for role in roles]}

    def get_queryset(self) -> Any:
        from app_main.views.logic.helpers import get_user_profile

        user_profile = get_user_profile(self.request, "self")
        self.searchtxt = "" or user_profile.searchtxt
        self.searchrole = "" or user_profile.searchrole
        from app_main.views.logic.helpers import get_users_after_search

        userlist: Any = get_users_after_search(self.searchtxt, self.searchrole)
        return userlist

    def get_context_data(
        self, *, object_list: Any = None, **kwargs: Any
    ) -> dict[str, Any]:
        ctx = super().get_context_data()
        ctx.update(
            {
                "stxt": self.searchtxt,
                "srole": self.searchrole,
            }
        )
        return ctx


class UserDetailView(ProfileSingleObjectMixin, generic.DetailView):
    model = Profile
    fields = "__all__"
    template_name = "app_main/userdetail.html"


class UserDeleteView(  # type: ignore
    LRMixin, RoleUPTMixin, generic.DeleteView
):
    role_required: str = "director"
    model = Profile
    success_url = "users/"

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        user_id = self.object.user_id
        usr = User.objects.get(id=user_id)
        usr.delete()
        return super().form_valid(form)


class UserUpdateView(ProfileSingleObjectMixin, generic.UpdateView):
    model = Profile
    fields = [
        "username",
        "name",
        "lastname",
        "email",
        "role",
    ]
    success_url = "/users"
    extra_context = {
        "roles": [role[0] for role in roles],
    }

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        user = self.object.user
        user.username, user.name, user.lastname, user.email = (
            form.data["username"],
            form.data["name"],
            form.data["lastname"],
            form.data["email"],
        )
        user.save()
        return super().form_valid(form)


class UserSearchView(LRMixin, generic.FormView):
    form_class = forms.Form
    template_name = "app_main/allusers.html"
    success_url = "/users/"

    def form_valid(self, form: forms.Form) -> Any:
        from app_main.views.logic.helpers import get_user_profile

        user_profile = get_user_profile(self.request, "self")
        if self.request.POST.get("searchrole") and not self.request.POST.get(
            "searchtxt"
        ):
            user_profile.searchrole = self.request.POST.get("searchrole", "")
        else:
            user_profile.searchtxt = self.request.POST.get("searchtxt", "")
            user_profile.searchrole = self.request.POST.get("searchrole", "")
        user_profile.save()
        return super().form_valid(form)


class UserSearchViewReset(LRMixin, generic.FormView):
    form_class = forms.Form
    template_name = "app_main/allusers.html"
    success_url = "/users/"

    def form_valid(self, form: forms.Form) -> Any:
        from app_main.views.logic.helpers import get_user_profile

        user_profile = get_user_profile(self.request, "self")
        if self.request.POST.get("clearsearch"):
            user_profile.searchtxt, user_profile.searchrole = "", ""
        elif self.request.POST.get("cleartxt"):
            user_profile.searchtxt = ""
        elif self.request.POST.get("clearrole"):
            user_profile.searchrole = ""
        user_profile.save()
        return super().form_valid(form)
