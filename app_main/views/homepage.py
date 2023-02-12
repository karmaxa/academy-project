from django import http
from django import views
from django.shortcuts import render


class HomeView(views.View):
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        return render(
            request,
            "app_main/index.html",
        )
