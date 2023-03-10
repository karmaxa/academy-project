from django import http
from django import views
from django.contrib.auth import get_user_model
from django.shortcuts import render

from app_main.mixins import LRMixin

User = get_user_model()


class HomeView(LRMixin, views.View):
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        try:
            acc = User.objects.get(id=self.request.user.pk)  # type: ignore
            from app_main.views.logic.helpers import get_user_profile

            prf = get_user_profile(self.request, "self")
        except User.DoesNotExist:
            acc = None
            prf = None
        return render(
            request,
            "app_main/index.html",
            {"acc": acc, "prf": prf},
        )
