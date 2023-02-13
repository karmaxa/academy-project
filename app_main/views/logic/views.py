from django.contrib.auth import get_user_model
from django.views import generic

from app_main.models import Profile

User = get_user_model()


class AllStudentsView(generic.ListView):
    template_name = "app_main/allstudents.html"
    model = Profile
