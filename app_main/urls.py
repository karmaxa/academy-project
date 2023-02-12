from django.urls import path

from app_main import views

app_name = "main"

urlpatterns = [
    path("", views.HomeView.as_view()),
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "login/success/", views.LoginSuccessful.as_view(), name="loginsuccess"
    ),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path("newuser/", views.UserSignUp.as_view(), name="newuser"),
]
