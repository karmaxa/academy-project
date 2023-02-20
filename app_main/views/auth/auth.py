from typing import Any

from django import forms
from django import http
from django import shortcuts
from django import views
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.views import generic

from app_main.forms import LogInForm
from app_main.forms import NewUserForm
from app_main.forms import SignUpForm
from app_main.mixins import LRMixin
from app_main.mixins import RoleUPTMixin
from app_main.models import Profile

User = get_user_model()


class LoginView(generic.FormView):
    template_name = "app_main/auth.html"
    form_class = LogInForm
    success_url = "/"

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        username = self.request.POST["username"]
        password = self.request.POST["password"]
        user = authenticate(self.request, username=username, password=password)
        nextq = self.request.GET.get("next", "")
        if nextq:
            self.request.session["next"] = nextq
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "successfully logged in")
            return shortcuts.redirect("success/")
        else:
            messages.error(self.request, "something went wrong")
            return shortcuts.redirect(f".?next={nextq}")

    def get_context_data(self, **kwargs: Any) -> dict:
        pctx = super().get_context_data()
        nextq = self.request.GET.get("next", None)
        if nextq:
            pctx["next"] = nextq
        return pctx


class LoginSuccessful(LRMixin, views.View):
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        nextq = request.session.get("next", "")
        if nextq:
            return shortcuts.redirect(nextq)
        else:
            return shortcuts.redirect("/")


class UserLogout(LRMixin, generic.FormView):
    template_name = "app_main/logoutpage.html"
    form_class = forms.Form
    success_url = "/"

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        logout(self.request)
        messages.warning(self.request, "successfully logged out")
        return super().form_valid(form)


def create_profile(user: Any, role: str) -> None:
    profile = Profile.objects.create(
        username=user.username,
        name=user.first_name,
        lastname=user.last_name,
        user=user,
        date=user.date_joined,
        marks={},
        role=role,
    )
    profile.save()


class UserSignUp(generic.FormView):
    template_name = "app_main/newuser.html"
    form_class = SignUpForm
    success_url = "/"

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        (username, firstname, lastname, password) = (
            form.cleaned_data["username"],
            form.cleaned_data["firstname"],
            form.cleaned_data["lastname"],
            form.cleaned_data["password"],
        )
        user = User.objects.create_user(username, password)
        user.first_name, user.last_name = firstname, lastname
        user.save()
        user_to_profile = User.objects.get(username=user.username)
        create_profile(user_to_profile, "student")
        userli = authenticate(
            self.request, username=username, password=password
        )
        login(request=self.request, user=userli)
        messages.warning(self.request, "successfully signed up")
        return shortcuts.redirect(self.success_url)


class NewUserCreate(LRMixin, RoleUPTMixin, generic.FormView):
    role_required = "director"

    template_name = "app_main/newuser.html"
    form_class = NewUserForm
    success_url = "/users/"

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        (username, firstname, lastname, password, role) = (
            form.cleaned_data["username"],
            form.cleaned_data["firstname"],
            form.cleaned_data["lastname"],
            form.cleaned_data["password"],
            form.cleaned_data["role"],
        )
        user = User.objects.create_user(username, password)
        user.first_name, user.last_name = firstname, lastname
        user.save()
        user_to_profile = User.objects.get(username=user.username)
        create_profile(user_to_profile, role)
        messages.warning(self.request, "created new user successfully")
        return shortcuts.redirect(self.success_url)
