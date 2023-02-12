from typing import Any

from django import forms
from django import http
from django import shortcuts
from django import views
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from app_main.forms import LogInForm


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
            return shortcuts.redirect("loginsuccess/")
        else:
            messages.error(self.request, "something went wrong")
            return shortcuts.redirect(f".?next={nextq}")

    def get_context_data(self, **kwargs: Any) -> dict:
        pctx = super().get_context_data()
        nextq = self.request.GET.get("next", None)
        if nextq:
            pctx["next"] = nextq
        return pctx


class LoginSuccessful(views.View):
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        nextq = request.session.get("next", "")
        if nextq:
            return shortcuts.redirect(nextq)
        else:
            return shortcuts.redirect("/")


class UserLogout(LoginRequiredMixin, generic.FormView):
    template_name = "app_main/logoutpage.html"
    form_class = forms.Form
    success_url = "/"

    def form_valid(self, form: forms.Form) -> http.HttpResponse:
        logout(self.request)
        messages.warning(self.request, "successfully logged out")
        return super().form_valid(form)
