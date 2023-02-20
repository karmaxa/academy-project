import datetime
from typing import Any

from django import http
from django import shortcuts
from django import views
from django.contrib.auth import get_user_model
from django.views import generic

from app_main import models
from app_main.helpers import marks
from app_main.views.logic import helpers
from app_main.views.mixins import LRMixin
from app_main.views.mixins import RoleUPTMixin

User = get_user_model()


class ClassesView(LRMixin, generic.ListView):
    model = models.ClassRoom
    template_name = "app_main/classeslist.html"


class ClassRoomView(LRMixin, generic.DetailView):
    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: dict
    ) -> http.HttpResponse:
        classroom = models.ClassRoom.objects.get(slug=kwargs.get("slug"))

        students = helpers.get_students_to_response(classroom)

        lessons, l_count = helpers.get_lessons_and_newlesid(classroom)

        user_role = helpers.get_user_role(request)

        current_student = helpers.get_current_student(
            request, classroom, "self"
        )

        response = shortcuts.render(
            self.request,
            "app_main/teacherclassroom.html",
            {
                "classroom": classroom,
                "students": students,
                "lessons": lessons,
                "marks": marks,
                "newles_title": "lesson" + str(l_count),
                "today": datetime.date.today().strftime("%Y-%m-%d"),
                "user_role": user_role,
                "current_student": current_student,
            },
        )
        return response


class ClassRoomEdit(LRMixin, RoleUPTMixin, views.View):
    role_required = "teacher"

    def post(
        self, request: http.HttpRequest, *args: Any, **kwargs: dict
    ) -> http.HttpResponseRedirect:
        classroom = models.ClassRoom.objects.get(slug=kwargs.get("slug"))
        user_role = helpers.get_user_role(request)

        if request.POST.get("newlesson"):
            helpers.add_new_lesson(request, classroom)

        elif user_role != "director":
            self.handle_no_permission("permission")
            return shortcuts.redirect(f"/classes/{kwargs.get('slug')}")

        if request.POST.get("commitchanges"):
            helpers.edit_classroom(request, classroom)

        if request.POST.get("deletelesson"):
            helpers.delete_lesson(request, classroom)

        return shortcuts.redirect(f"/classes/{kwargs.get('slug')}")
