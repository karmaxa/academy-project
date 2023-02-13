from django.contrib.auth import get_user_model
from django.views import generic

from app_main.models import Profile

User = get_user_model()


class AllUsersView(generic.ListView):
    template_name = "app_main/allusers.html"
    model = Profile
