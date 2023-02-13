from django import forms
from django import http
from django.contrib.auth import get_user_model
from django.views import generic

from app_main.models import Profile
from app_main.views import LRMixin
from app_main.views.mixins import RoleUPTMixin

User = get_user_model()


class AllUsersView(LRMixin, RoleUPTMixin, generic.ListView):
    role_required: str = "director"
    template_name = "app_main/allusers.html"
    model = Profile


class UserDetailView(LRMixin, RoleUPTMixin, generic.DetailView):
    role_required: str = "director"
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


class UserUpdateView(LRMixin, RoleUPTMixin, generic.UpdateView):
    role_required: str = "director"
    model = Profile
