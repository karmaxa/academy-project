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
    path("signup/", views.UserSignUp.as_view(), name="signup"),
    path("newuser/", views.NewUserCreate.as_view(), name="newuser"),
    path("users/", views.AllUsersView.as_view(), name="users"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="userdetail"),
    path(
        "users/<int:pk>/delete/",
        views.UserDeleteView.as_view(),
        name="userdelete",
    ),
]
