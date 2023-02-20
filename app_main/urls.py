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
    path("profile/", views.UserDetailView.as_view(), name="profile"),
    path("profile/edit/", views.UserUpdateView.as_view(), name="editprofile"),
    path("users/", views.AllUsersView.as_view(), name="users"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="userdetail"),
    path(
        "users/<int:pk>/delete/",
        views.UserDeleteView.as_view(),
        name="userdelete",
    ),
    path(
        "users/<int:pk>/edit/",
        views.UserUpdateView.as_view(),
        name="useredit",
    ),
    path(
        "users/search/",
        views.UserSearchView.as_view(),
        name="usersearch",
    ),
    path(
        "users/search/reset/",
        views.UserSearchViewReset.as_view(),
        name="usersearchreset",
    ),
    path("classes/", views.ClassesView.as_view(), name="classrooms"),
    path(
        "classes/<slug:slug>/", views.ClassRoomView.as_view(), name="classroom"
    ),
    path(
        "classes/<slug:slug>/editlesson/",
        views.ClassRoomEdit.as_view(),
        name="editlesson",
    ),
]
